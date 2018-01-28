#!/usr/bin/env python3
import os
import distutils
from setuptools import setup
from setuptools.command.install import install as _install


with open('README.rst') as readme_file:
    readme = readme_file.read()


PTH = """\
try:
    import alljson
except ImportError:
    pass
"""


# stolen from: https://github.com/asottile/future-fstrings/
class install(_install):
    def initialize_options(self):
        _install.initialize_options(self)
        # Use this prefix to get loaded as early as possible
        name = 'aaaaa_' + self.distribution.metadata.name
        contents = 'import sys; exec({!r})\n'.format(PTH)
        self.extra_path = (name, contents)

    def finalize_options(self):
        _install.finalize_options(self)

        install_suffix = os.path.relpath(
            self.install_lib, self.install_libbase,
        )
        if install_suffix == '.':
            distutils.log.info('skipping install of .pth during easy-install')
        elif install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase
            distutils.log.info(
                "will install .pth to '%s.pth'",
                os.path.join(self.install_lib, self.extra_path[0]),
            )
        else:
            raise AssertionError(
                'unexpected install_suffix',
                self.install_lib, self.install_libbase, install_suffix,
            )


setup(
    name='alljson',
    version='0.1',
    description='Make any type JSON-serializable',
    long_description=readme,
    author='Marcin Bachry',
    author_email='hegel666@gmail.com',
    url='https://github.com/mbachry/alljson',
    py_modules=['alljson'],
    install_requires=[
        'six',
    ],
    cmdclass={'install': install},
    license='MIT',
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
