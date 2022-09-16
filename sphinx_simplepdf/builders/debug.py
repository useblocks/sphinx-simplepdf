import sys
import pkgutil
import pkg_resources
import platform

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
                version = pkg_resources.get_distribution(name).version
            except (Exception):
                final[name] = 'unknown'
            else:
                final[name] = version

        return final

    @property
    def os(self):
        return platform.system(), platform.release()
