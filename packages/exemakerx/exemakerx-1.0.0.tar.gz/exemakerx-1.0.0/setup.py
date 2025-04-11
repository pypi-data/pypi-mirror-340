from setuptools import setup, find_packages

setup(
    name="exemakerx",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyinstaller"
    ],
    entry_points={
        'console_scripts': [
            'exemakerx = exemakerx.__main__:main'
        ]
    },
    author="Ruzgar",
    description="Convert .py files to .exe with GUI and CLI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruzgar/exemakerx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)