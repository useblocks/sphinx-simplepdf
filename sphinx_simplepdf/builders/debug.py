from importlib.metadata import version
import pkgutil
import platform
import sys


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
                _package_version = version(name)
            except Exception:
                final[name] = "unknown"
            else:
                final[name] = _package_version

        return final

    @property
    def os(self):
        return platform.system(), platform.release()
