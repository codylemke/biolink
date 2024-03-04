from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here.
        # Examples:
        # 'numpy>=1.19.2',
        # 'requests>=2.24.0',
    ],
    # Additional metadata about your package.
    author='Your Name',
    author_email='your.email@example.com',
    description='A description of your project',
    # Consider adding classifiers to provide more metadata.
    # Check https://pypi.org/classifiers/ for a list of valid classifiers.
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)