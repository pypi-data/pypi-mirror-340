from setuptools import setup, find_packages

setup(
    name='lmc_library_management_system',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'library_management = main:main'
        ]
    }
)
