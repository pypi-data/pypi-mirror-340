from setuptools import setup, find_packages

setup(
    name='garrett-status',
    version='0.1.1',
    description='Garrett Remote Desktop Status Viewer',
    author='Maroti Belge',
    author_email='maroti.belge@tatatecchnologies.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
    entry_points={
        'console_scripts': [
            'garrett-status=garrett_status:run'
        ],
    },
    python_requires='>=3.6',
)
