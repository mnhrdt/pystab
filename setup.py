from setuptools import setup, Extension
from sysconfig import get_config_var
from subprocess import check_output
import sys

extra_compile_args = get_config_var('CFLAGS').split()

extra_link_args = []
if sys.platform == "darwin":
    extra_link_args = ["-L /usr/local/lib"]

extensions = [Extension("libstab",
                        ["stab/stab.c"],
                        include_dirs=['stab', "/usr/local/include"],
                        library_dirs=["/usr/local/lib"],
                        extra_compile_args=extra_compile_args,
                        extra_link_args=extra_link_args,
                        depends=["stab/stab.h"])]

# from https://stackoverflow.com/a/38525461
from distutils.command.install_lib import install_lib as _install_lib
import os
import re
def batch_rename(src, dst, src_dir_fd=None, dst_dir_fd=None):
    '''Same as os.rename, but returns the renaming result.'''
    os.rename(src, dst,
              src_dir_fd=src_dir_fd,
              dst_dir_fd=dst_dir_fd)
    return dst

class _CommandInstall(_install_lib):
    def __init__(self, *args, **kwargs):
        _install_lib.__init__(self, *args, **kwargs)

    def install(self):
        # let the distutils' install_lib do the hard work
        outfiles = _install_lib.install(self)
        # batch rename the outfiles:
        # for each file, match string between
        # second last and last dot and trim it
        matcher = re.compile('\.([^.]+)\.so$')
        return [batch_rename(file, re.sub(matcher, '.so', file))
                for file in outfiles]

setup(name="stab",
      version='1',
      author="Enric Meinhardt-Llopis",
      author_email="enric.meinhardt@fastmail.com",
      description="Python wrapper of C functions for stable distributions",
      url='https://github.com/mnhrdt/pystab',
      classifiers=[
          "Operating System :: OS Independent",
      ],
      py_modules=['stab'],
      ext_modules=extensions,
      cmdclass={
          'install_lib': _CommandInstall,
      },
)

