from setuptools import setup, find_packages

setup(
    name="smuxent",
    version="0.0.2",
    description="Native threading for Python using C++ and pybind11",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Patryk Wrzesniewski",
    license="MIT License (MIT)",
    url="https://github.com/Patrykkw/Smuxent",
    project_urls={
        "Source": "https://github.com/Patrykkw/Smuxent",
        "Bug Tracker": "https://github.com/Patrykkw/Smuxent/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    python_requires=">=3.11,<3.13",
)

