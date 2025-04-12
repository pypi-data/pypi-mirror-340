from setuptools import setup, find_packages

setup(
    name='tiana_data_structures',
    version="0.0.1",
    description='Python package that implements common data structures.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rabemanantsoa Andriamianja Tiana',
    author_email='arabemanantsoa@aimsammi.org',
    url='https://github.com/Mianja-Tiana/',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)