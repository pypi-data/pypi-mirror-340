import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leeselab-project-creator",
    version="2.0.0",
    author="Dominik Buchner",
    author_email="dominik.buchner524@googlemail.com",
    description="The leeselab project creator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DominikBuchner/BOLDigger-commandline",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=[
        "openpyxl>=3.1.1",
        "pandas>=1.5.3",
        "FreeSimpleGUI >= 5",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "leeselab-project-creator = leeselab_project_creator.__main__:main",
        ]
    },
)
