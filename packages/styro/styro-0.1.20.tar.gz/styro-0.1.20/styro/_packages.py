__version__ = "0.1.19"

import asyncio
import contextlib
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Union

if sys.version_info >= (3, 9):
    from collections.abc import Generator
else:
    from typing import Generator

import aiohttp
import typer

from ._git import clone, fetch
from ._openfoam import openfoam_version, platform_path
from ._self import (
    check_for_new_version,
    is_managed_installation,
    print_upgrade_instruction,
    selfupgrade,
)
from ._status import Status
from ._subprocess import run
from ._util import path_from_uri, reentrantcontextmanager


@reentrantcontextmanager
def _lock() -> Generator[Dict[str, Any], None, None]:
    installed_path = platform_path() / "styro" / "installed.json"

    installed_path.parent.mkdir(parents=True, exist_ok=True)
    installed_path.touch(exist_ok=True)
    with installed_path.open("r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)

        try:
            f.seek(0)
            installed = json.load(f)
        except json.JSONDecodeError:
            installed = {}
        else:
            assert isinstance(installed, dict)
            if installed.get("version") != 1:
                typer.echo(
                    "🛑 Error: installed.json file is of a newer version. Please upgrade styro.",
                    err=True,
                )
                print_upgrade_instruction()
                raise typer.Exit(code=1)
        installed_copy = deepcopy(installed)
        try:
            yield installed
        finally:
            if installed:
                if installed != installed_copy:
                    f.seek(0)
                    f.write(json.dumps(installed, indent=2))
                    f.truncate()
            else:
                installed_path.unlink()


lock = _lock()


class Package:
    __instances: ClassVar[Dict[str, "Package"]] = {}
    __install_lock: ClassVar[asyncio.Lock] = asyncio.Lock()
    __name_regex: ClassVar[re.Pattern] = re.compile(
        r"^(?!.*--)[a-z0-9]+(-[a-z0-9]+)*$",
    )

    @staticmethod
    def _check_for_duplicate_names(pkgs: Set["Package"]) -> None:
        names = {pkg.name for pkg in pkgs}
        if len(names) != len(pkgs):
            typer.echo(
                "🛑 Error: Duplicate package names found.",
                err=True,
            )
            raise typer.Exit(code=1)

    @staticmethod
    def installed() -> Set["Package"]:
        with lock as installed:
            return {Package(name) for name in installed.get("packages", {})}

    @staticmethod
    @lock
    async def resolve_all(
        pkgs: Set["Package"],
        *,
        upgrade: bool = False,
    ) -> Set["Package"]:
        Package._check_for_duplicate_names(pkgs)

        resolved: Set[Package] = set()
        return {
            pkg
            for pkgs in await asyncio.gather(
                *(pkg.resolve(upgrade=upgrade, _resolved=resolved) for pkg in pkgs),
            )
            for pkg in pkgs
        }

    @staticmethod
    @lock
    async def install_all(pkgs: Set["Package"], *, upgrade: bool = False) -> None:
        to_install = {
            pkg: asyncio.Event()
            for pkg in await Package.resolve_all(pkgs, upgrade=upgrade)
        }

        not_to_install = pkgs.difference(to_install)

        await asyncio.gather(
            *(pkg.install(upgrade=upgrade, _deps=False) for pkg in not_to_install),
            *(
                pkg.install(_force_reinstall=True, _deps=to_install)
                for pkg in to_install
            ),
        )

    @staticmethod
    @lock
    async def uninstall_all(pkgs: Set["Package"]) -> None:
        dependents = set()
        for pkg in pkgs:
            dependents.update(pkg.installed_dependents())
        dependents -= pkgs
        if dependents:
            typer.echo(
                f"🛑 Error: Cannot uninstall {','.join([pkg.name for pkg in pkgs])}: required by {','.join([dep.name for dep in dependents])}",
                err=True,
            )
            raise typer.Exit(code=1)

        await asyncio.gather(
            *(pkg.uninstall(_force=True) for pkg in pkgs),
        )

    def __new__(cls, package: str) -> "Package":
        if cls is not Package:
            return super().__new__(cls)

        with lock as installed:
            name = package.lower().replace("_", "-")
            if Package.__name_regex.match(name):
                package = name
                with contextlib.suppress(KeyError):
                    package = installed["packages"][name]["origin"]

            try:
                return Package.__instances[package]
            except KeyError:
                if package.startswith((".", "/", "~", "file://")):
                    instance: Package = super().__new__(_LocalPackage)
                elif package.startswith(("http://", "https://")):
                    instance = super().__new__(_GitPackage)
                elif package == "styro":
                    instance = super().__new__(_Styro)
                else:
                    instance = super().__new__(_IndexedPackage)

                Package.__instances[package] = instance

                return instance

    def __init__(self, name: str) -> None:
        if not hasattr(self, "name"):
            name = name.lower().replace("_", "-")
            if not Package.__name_regex.match(name):
                msg = f"Invalid package name: {name}"
                raise ValueError(msg)
            if name == "styro" and not isinstance(self, _Styro):
                msg = "'styro' not allowed as a package name."
                raise ValueError(msg)
            self.name = name
            self._origin: Optional[Union[str, Path]] = None
            self._metadata: Optional[Dict[str, Any]] = None
            self._upgrade_available = False

    def _build_steps(self) -> List[str]:
        assert self._metadata is not None

        build = self._metadata.get("build", "wmake")

        if build == "wmake":
            build = ["wmake all -j"]
        elif isinstance(build, str):
            typer.echo(
                f"🛑 Error: Unsupported build system: {build}.",
                err=True,
            )
            raise typer.Exit(code=1)

        return build

    def _check_compatibility(self) -> None:
        assert self._metadata is not None

        distro_compatible = False
        specs = self._metadata.get("version", [])
        for spec in specs:
            try:
                if spec.startswith("=="):
                    version = int(spec[2:])
                    compatible = openfoam_version() == version
                elif spec.startswith("!="):
                    version = int(spec[2:])
                    compatible = openfoam_version() != version
                elif spec.startswith(">="):
                    version = int(spec[2:])
                    compatible = openfoam_version() >= version
                elif spec.startswith(">"):
                    version = int(spec[1:])
                    compatible = openfoam_version() > version
                elif spec.startswith("<="):
                    version = int(spec[2:])
                    compatible = openfoam_version() <= version
                elif spec.startswith("<"):
                    version = int(spec[1:])
                    compatible = openfoam_version() < version
                else:
                    typer.echo(
                        f"⚠️ Warning: {self.name}: ignoring invalid version specifier '{spec}'.",
                        err=True,
                    )
                    continue
            except ValueError:
                typer.echo(
                    f"⚠️ Warning: {self.name}: ignoring invalid version specifier '{spec}'.",
                    err=True,
                )
                continue

            if (openfoam_version() < 1000) == (version < 1000):  # noqa: PLR2004
                distro_compatible = True
                if not compatible:
                    typer.echo(
                        f"🛑 Error: OpenFOAM version is {openfoam_version()}, but {self.name} requires {spec}.",
                        err=True,
                    )
                    raise typer.Exit(code=1)

        if specs and not distro_compatible:
            typer.echo(
                f"🛑 Error: {self.name} is not compatible with this OpenFOAM distribution (requires {', '.join(specs)}).",
                err=True,
            )
            raise typer.Exit(code=1)

    async def fetch(self) -> None:
        raise NotImplementedError

    async def resolve(
        self,
        *,
        upgrade: bool = False,
        _force_reinstall: bool = False,
        _resolved: Optional[Set["Package"]] = None,
    ) -> Set["Package"]:
        if _resolved is None:
            _resolved = set()
        elif self in _resolved:
            return set()

        _resolved.add(self)

        if self.installed_sha() is not None and not upgrade and not _force_reinstall:
            return set()

        if self._metadata is None:
            await self.fetch()
            assert self._metadata is not None
            self._check_compatibility()
            self._build_steps()

        if (
            self.installed_sha() is not None
            and not self._upgrade_available
            and not _force_reinstall
        ):
            return set()

        ret = {self}

        dependencies = await asyncio.gather(
            *(
                dep.resolve(upgrade=True, _resolved=_resolved)
                for dep in self.dependencies()
            ),
            *(
                dep.resolve(_force_reinstall=True, _resolved=_resolved)
                for dep in self.installed_dependents()
            ),
        )
        for deps in dependencies:
            ret.update(deps)

        return ret

    def is_installed(self) -> bool:
        return self in self.installed()

    def installed_apps(self) -> Set[Path]:
        with lock as installed:
            try:
                return {
                    Path(platform_path() / "bin" / app)
                    for app in installed["packages"][self.name]["apps"]
                }
            except KeyError:
                return set()

    def installed_libs(self) -> Set[Path]:
        with lock as installed:
            try:
                return {
                    Path(platform_path() / "lib" / lib)
                    for lib in installed["packages"][self.name]["libs"]
                }
            except KeyError:
                return set()

    def installed_sha(self) -> Optional[str]:
        with lock as installed:
            try:
                return installed["packages"][self.name]["sha"]
            except KeyError:
                return None

    def dependencies(self) -> Set["Package"]:
        assert self._metadata is not None
        return {Package(name) for name in self._metadata.get("requires", [])}

    def installed_dependents(self) -> Set["Package"]:
        with lock as installed:
            return {
                Package(name)
                for name, data in installed.get("packages", {}).items()
                if self.name in data.get("requires", [])
            }

    @property
    def _pkg_path(self) -> Path:
        return platform_path() / "styro" / "pkg" / self.name

    async def download(self) -> Optional[str]:
        raise NotImplementedError

    async def install(
        self,
        *,
        upgrade: bool = False,
        _force_reinstall: bool = False,
        _deps: Union[bool, Dict["Package", asyncio.Event]] = True,
    ) -> None:
        with lock as installed:
            if _deps is True:
                await self.install_all({self}, upgrade=upgrade)
                return

            if (
                self.is_installed()
                and not isinstance(self, _LocalPackage)
                and not upgrade
                and not _force_reinstall
            ):
                typer.echo(
                    f"✋ Package '{self.name}' is already installed.",
                )
                return

            if self._metadata is None:
                await self.fetch()
                assert self._metadata is not None
                self._check_compatibility()

            if (
                self.is_installed()
                and not isinstance(self, _LocalPackage)
                and not self._upgrade_available
                and not _force_reinstall
            ):
                typer.echo(
                    f"✋ Package '{self.name}' is already up-to-date.",
                )
                return

            sha = await self.download()

            if self.name in installed.get("packages", {}):
                await self.uninstall(_force=True, _keep_pkg=True)
                assert self.name not in installed.get("packages", {})
            assert not self.is_installed()

            if isinstance(_deps, dict):
                dependencies = self.dependencies()
                await asyncio.gather(
                    *(
                        event.wait()
                        for pkg, event in _deps.items()
                        if pkg in dependencies
                    )
                )

            async with self.__install_lock:
                with Status(f"⏳ Installing {self.name}") as status:
                    installed_apps = {
                        app
                        for p in installed.get("packages", {})
                        for app in installed.get("packages", {})[p].get("apps", [])
                    }
                    installed_libs = {
                        lib
                        for p in installed.get("packages", {})
                        for lib in installed.get("packages", {})[p].get("libs", [])
                    }

                    try:
                        current_apps = {
                            f: f.stat().st_mtime
                            for f in (platform_path() / "bin").iterdir()
                            if f.is_file()
                        }
                    except FileNotFoundError:
                        current_apps = {}
                    try:
                        current_libs = {
                            f: f.stat().st_mtime
                            for f in (platform_path() / "lib").iterdir()
                            if f.is_file()
                        }
                    except FileNotFoundError:
                        current_libs = {}

                    if self.dependencies():
                        env = os.environ.copy()
                        env["OPI_DEPENDENCIES"] = str(self._pkg_path.parent)
                    else:
                        env = None

                    for cmd in self._build_steps():
                        try:
                            await run(
                                ["/bin/bash", "-c", cmd],
                                cwd=self._pkg_path,
                                env=env,
                                status=status,
                            )
                        except subprocess.CalledProcessError as e:
                            typer.echo(
                                f"🛑 Error: failed to build package '{self.name}'\n{e.stderr}",
                                err=True,
                            )

                            try:
                                new_apps = sorted(
                                    f
                                    for f in (platform_path() / "bin").iterdir()
                                    if f.is_file()
                                    and f not in installed_apps
                                    and (
                                        f not in current_apps
                                        or f.stat().st_mtime > current_apps[f]
                                    )
                                )
                            except FileNotFoundError:
                                new_apps = []

                            try:
                                new_libs = sorted(
                                    f
                                    for f in (platform_path() / "lib").iterdir()
                                    if f.is_file()
                                    and f not in installed_libs
                                    and (
                                        f not in current_libs
                                        or f.stat().st_mtime > current_libs[f]
                                    )
                                )
                            except FileNotFoundError:
                                new_libs = []

                            for app in new_apps:
                                with contextlib.suppress(FileNotFoundError):
                                    app.unlink()

                            for lib in new_libs:
                                with contextlib.suppress(FileNotFoundError):
                                    lib.unlink()

                            shutil.rmtree(self._pkg_path, ignore_errors=True)

                            raise typer.Exit(code=1) from e

                        try:
                            new_apps = sorted(
                                f
                                for f in (platform_path() / "bin").iterdir()
                                if f.is_file() and f not in current_apps
                            )
                        except FileNotFoundError:
                            new_apps = []

                        try:
                            new_libs = sorted(
                                f
                                for f in (platform_path() / "lib").iterdir()
                                if f.is_file() and f not in current_libs
                            )
                        except FileNotFoundError:
                            new_libs = []

                        if not installed:
                            installed["version"] = 1
                            installed["packages"] = {}

                        installed["packages"][self.name] = {
                            "apps": [app.name for app in new_apps],
                            "libs": [lib.name for lib in new_libs],
                        }
                        if sha is not None:
                            installed["packages"][self.name]["sha"] = sha
                        if self.dependencies():
                            installed["packages"][self.name]["requires"] = [
                                dep.name for dep in self.dependencies()
                            ]
                        if isinstance(self._origin, Path):
                            installed["packages"][self.name]["origin"] = (
                                self._origin.as_uri()
                            )
                        elif isinstance(self._origin, str):
                            installed["packages"][self.name]["origin"] = self._origin

                self._upgrade_available = False

                typer.echo(f"✅ Package '{self.name}' installed successfully.")

                if new_libs:
                    typer.echo("⚙️ New libraries:")
                    for lib in new_libs:
                        typer.echo(f"  {lib.name}")

                if new_apps:
                    typer.echo("🖥️ New applications:")
                    for app in new_apps:
                        typer.echo(f"  {app.name}")

            if isinstance(_deps, dict):
                _deps[self].set()

    async def uninstall(
        self,
        *,
        _force: bool = False,
        _keep_pkg: bool = False,
    ) -> None:
        if not _force:
            assert not _keep_pkg
            await self.uninstall_all({self})

        with lock as installed:
            if self.name not in installed.get("packages", {}):
                typer.echo(
                    f"⚠️ Warning: skipping package '{self.name}' as it is not installed.",
                    err=True,
                )
                return

            with Status(f"⏳ Uninstalling {self.name}"):
                for app in self.installed_apps():
                    with contextlib.suppress(FileNotFoundError):
                        app.unlink()

                for lib in self.installed_libs():
                    with contextlib.suppress(FileNotFoundError):
                        lib.unlink()

                if not _keep_pkg:
                    shutil.rmtree(
                        self._pkg_path,
                        ignore_errors=True,
                    )

                with contextlib.suppress(KeyError):
                    del installed["packages"][self.name]

        assert not self.is_installed()

        typer.echo(f"🗑️ Package '{self.name}' uninstalled successfully.")

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Package):
            return NotImplemented
        return self.name == other.name and self._origin == other._origin

    def __hash__(self) -> int:
        return hash((self.name, self._origin))


class _IndexedPackage(Package):
    async def fetch(self) -> None:
        with Status(f"🔍 Fetching {self}"):
            try:
                async with aiohttp.ClientSession(
                    raise_for_status=True
                ) as session, session.get(
                    f"https://raw.githubusercontent.com/exasim-project/opi/main/pkg/{self.name}/metadata.json"
                ) as response:
                    self._metadata = await response.json(content_type="text/plain")
            except Exception as e:
                typer.echo(
                    f"🛑 Error: Failed to fetch package '{self.name}': {e}",
                    err=True,
                )
                raise typer.Exit(code=1) from e

        assert self._metadata is not None

        new_sha = await fetch(self._pkg_path, self._metadata["repo"])
        if new_sha is None:
            self._upgrade_available = True
        else:
            self._upgrade_available = new_sha != self.installed_sha()

    async def download(self) -> str:
        assert self._metadata is not None
        if self.is_installed():
            title = f"⏩ Updating {self.name}"
        else:
            title = f"⏬ Downloading {self.name}"
        with Status(title):
            return await clone(self._pkg_path, self._metadata["repo"])


class _GitPackage(Package):
    def __init__(self, package: str) -> None:
        if not package.startswith(("http://", "https://")):
            package = package.lower().replace("_", "-")
            with lock as installed:
                package = installed["packages"][package]["origin"]

        super().__init__(package.rsplit("/", 1)[-1].split(".", 1)[0])
        self._origin = package

    async def fetch(self) -> None:
        with Status(f"⏬ Downloading {self}"):
            assert isinstance(self._origin, str)
            new_sha = await fetch(self._pkg_path, self._origin, missing_ok=False)
        assert new_sha is not None
        branch = (
            await run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self._pkg_path,
            )
        ).stdout.strip()
        await run(["git", "checkout", new_sha], cwd=self._pkg_path)
        try:
            self._metadata = json.loads((self._pkg_path / "metadata.json").read_text())
        except FileNotFoundError:
            self._metadata = {}
        finally:
            await run(["git", "checkout", branch], cwd=self._pkg_path)
        self._upgrade_available = new_sha != self.installed_sha()

    async def download(self) -> str:
        assert isinstance(self._origin, str)
        return await clone(self._pkg_path, self._origin)

    def __str__(self) -> str:
        return f"{self.name} @ {self._origin}"


class _LocalPackage(Package):
    def __init__(self, package: str) -> None:
        if not package.startswith((".", "/", "~", "file://")):
            package = package.lower().replace("_", "-")
            with lock as installed:
                package = installed["packages"][package]["origin"]

        if package.startswith("file://"):
            path = path_from_uri(package)
        else:
            path = Path(package).absolute()
        super().__init__(path.name)
        self._origin = path

    async def fetch(self) -> None:
        try:
            assert isinstance(self._origin, Path)
            self._metadata = json.loads((self._origin / "metadata.json").read_text())
        except FileNotFoundError:
            self._metadata = {}
        self._upgrade_available = True

    async def download(self) -> None:
        assert self._metadata is not None
        assert isinstance(self._origin, Path)
        shutil.rmtree(self._pkg_path, ignore_errors=True)
        self._pkg_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            self._origin,
            self._pkg_path,
        )

    def __str__(self) -> str:
        assert isinstance(self._origin, Path)
        return f"{self.name} @ {self._origin.as_uri()}"


class _Styro(Package):
    def __init__(self, package: str) -> None:
        assert package.lower() == "styro"
        super().__init__("styro")

    def is_installed(self) -> bool:
        return True

    async def resolve(
        self,
        *,
        upgrade: bool = False,
        _force_reinstall: bool = False,
        _resolved: Optional[Set["Package"]] = None,
    ) -> Set["Package"]:
        if not upgrade and not _force_reinstall:
            return set()

        self._upgrade_available = await check_for_new_version(verbose=False)

        if not _force_reinstall and not self._upgrade_available:
            return set()

        if is_managed_installation():
            typer.echo(
                "🛑 Error: this is a managed installation of styro.",
                err=True,
            )
            print_upgrade_instruction()
            raise typer.Exit(code=1)

        return {self}

    async def install(
        self,
        *,
        upgrade: bool = False,
        _force_reinstall: bool = False,
        _deps: Union[bool, Dict[Package, asyncio.Event]] = True,
    ) -> None:
        if not upgrade and not _force_reinstall:
            typer.echo(
                "✋ Package 'styro' is already installed.",
            )
            return

        if is_managed_installation():
            typer.echo(
                "🛑 Error: this is a managed installation of styro.",
                err=True,
            )
            print_upgrade_instruction()
            raise typer.Exit(code=1)

        self._upgrade_available = await check_for_new_version(verbose=False)

        if not _force_reinstall and not self._upgrade_available:
            typer.echo(
                "✋ Package 'styro' is already up-to-date.",
            )
            return

        await selfupgrade()

        typer.echo("✅ Package 'styro' upgraded successfully.")

    async def uninstall(self, *, _force: bool = False, _keep_pkg: bool = False) -> None:
        typer.echo(
            "🛑 Error: styro cannot be uninstalled this way.",
            err=True,
        )
        if is_managed_installation():
            typer.echo(
                "💡 Use your package manager (e.g. pip) to uninstall styro.",
                err=True,
            )
        else:
            typer.echo(
                "💡 Delete the 'styro' binary in $FOAM_USER_APPBIN to uninstall.",
                err=True,
            )
        raise typer.Exit(code=1)
