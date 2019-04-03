import ctypes
import os
from os import environ as env
def fix_mesh_generation_time(firedrake_install_path):
    """For some reason, the current install script for Complex on Balena
    (the University of Bath's high performance computer) takes a very
    long time to generate meshes. This code appears to fix the problem,
    and was suggested my Michal Habera -
    https://wwwen.uni.lu/recherche/fstc/
    research_unit_in_engineering_sciences_rues/members/michal_habera.

    Parameters:

    :param:firedrake_install_path: A string giving the path to the
    current firedrake install. Must end in '/'.
    """



    dir_and_arch =  get_petsc_dir()

    petsc_dir = dir_and_arch[0]

    try:
        petsc_arch = dir_and_arch[1]
    except IndexError:
        petsc_arch = ''
    
    libpetsc_path = os.path.join(petsc_dir, petsc_arch, 'lib', 'libpetsc.so')

    petsc = ctypes.CDLL(libpetsc_path)

    # Do not check validity of address before dereferencing pointers

    petsc.PetscCheckPointerSetIntensity(0)

def get_petsc_dir():
    try:
        petsc_arch = env.get('PETSC_ARCH', '')
        petsc_dir = env['PETSC_DIR']
        if petsc_arch:
            return (petsc_dir, path.join(petsc_dir, petsc_arch))
        return (petsc_dir,)
    except KeyError:
        try:
            import petsc
            return (petsc.get_petsc_dir(), )
        except ImportError:
            sys.exit("""Error: Could not find PETSc library.
Set the environment variable PETSC_DIR to your local PETSc base
directory or install PETSc from PyPI as described in the manual:
http://firedrakeproject.org/obtaining_pyop2.html#petsc
""")

# Above code taken from
# Firedrake project at
# https://github.com/firedrakeproject/firedrake/blob/46681927e3194d587e09684a49a952ae3cc68269/setup.py,
# used under LGPLv3
