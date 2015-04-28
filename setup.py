__author__ = 'Xiangru Lian'
from cx_Freeze import setup, Executable

buildOptions = {
    'includes':[r'scipy.sparse.csgraph._validation', r'scipy.special._ufuncs_cxx', r'scipy.integrate.vode', r'scipy.integrate.lsoda'],
    'packages':[],
    'include_files':[r'libifcoremd.dll', r'libmmd.dll']}

executables = [Executable(script='MainWindow.py', base="Win32GUI",)] # base for not showing terminal

setup(name= 'NmrAnalysis',
      version = '1.0',
      description = 'Analysis System by iceorange',
      options = dict(build_exe = buildOptions),
      executables = executables
      )

# from distutils.core import setup
# import py2exe
#
# setup(console= ['MainWindow.py'],
#       options={
#         'py2exe': {
#             r'includes': [r'scipy.sparse.csgraph._validation',
#                           r'scipy.special._ufuncs_cxx']
#         }
#     })