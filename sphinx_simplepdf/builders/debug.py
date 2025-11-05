import pkgutil
import platform
import sys

from importlib.metadata import version, PackageNotFoundError


class DebugPython:
    @property
    def py_exec(self):
        return sys.executable

    def get_packages(self):
        packages = list(pkgutil.iter_modules())

        names = [x[1] for x in packages]

        final = {}
        for name in names:
            try:
                pkg_version = version(name)
            except PackageNotFoundError:
                final[name] = "unknown"
            else:
                final[name] = pkg_version

        return final

    @property
    def os(self):
        return platform.system(), platform.release()
