from setuptools import setup, find_packages

setup(
    name="pyrtk-cli",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "fastapi",
        "uvicorn",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "pyrtk=pyrtk.main:main",
        ],
    },
    author="Andres Mardones",
    description="A modern CLI for scaffolding and managing FastAPI projects with clean architecture.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Framework :: FastAPI"
    ],
    python_requires='>=3.7',
)