from distutils.core import setup

setup(
    name = 'kinematics',
    version = '1.0',
    description = 'kinematics library',
    author = 'aiden',
    packages = ['kinematics'],
    package_data = {
        'kinematics': ['*.so'], 
    }
)
