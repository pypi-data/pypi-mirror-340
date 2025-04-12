from setuptools import setup, find_packages
from typing import List

# Constant for editable install, which we’ll remove from requirements
HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """Reads a requirements file and returns a cleaned list of dependencies."""
    requirements = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Skip empty lines or comments
            if not line or line.startswith("#"):
                continue

            # Skip editable installs
            if line == HYPEN_E_DOT:
                continue

            requirements.append(line)

    return requirements

# Read long description from README.md for PyPI display
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Package metadata
__version__ = "0.0.11"
REPO_NAME = "mlops2"
PKG_NAME = "database_mongodb"
AUTHOR_USER_NAME = "Abdoul1996"
AUTHOR_EMAIL = "aabdillahid@gmail.com"

# Main setup function
setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package for connecting with MongoDB.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},                        # Use 'src' layout
    packages=find_packages(where="src"),            # Find all packages in src/
    install_requires=[
    "pymongo[srv]",
    "dnspython",
    "pandas",
    "numpy",
    "ensure"
],  # Read dependencies from file
    include_package_data=True,                      # Include files from MANIFEST.in if any
    classifiers=[                                   # Optional: add classifiers here or via setup.cfg
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
