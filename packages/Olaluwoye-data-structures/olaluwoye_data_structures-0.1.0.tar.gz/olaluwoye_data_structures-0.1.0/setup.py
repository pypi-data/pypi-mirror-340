from setuptools import setup, find_packages

# Reading the contents of README.md for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="Olaluwoye-data-structures",  # Package name
    version="0.1.0",  # Package version
    description="A Python package implementing core data structures from scratch using object-oriented Python",
    long_description=long_description,  # Read the contents of README.md for long description
    long_description_content_type="text/markdown",  # This tells setuptools that the README is in markdown format
    author="Olaluwoye Olalekan",  # Author's name
    author_email="olaluwoye9@gmail.com",  # Author's email
    url="https://github.com/olaluwoye9/Olaluwoye-data-structures",  # GitHub repo URL
    license="MIT",  # License
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="data_structures"),  # This finds and includes all the necessary packages in the `data_structures` folder
    python_requires=">=3.6",  # Python version requirement
    install_requires=[],  # Add any dependencies your project needs here
    package_data={  # This is where you specify extra files to be included (e.g., images, config files)
        # Include any extra data files your package needs here
        # Example:
        # 'data_structures': ['data/*.dat'],
    },
    entry_points={  # If your project has command-line tools, specify them here
        # Example:
        # 'console_scripts': [
        #     'my-script = my_module.script:main_function',
        # ],
    },
    include_package_data=True,  # Include non-Python files if specified
    zip_safe=False,  # Whether to allow packaging into a .egg file
)
