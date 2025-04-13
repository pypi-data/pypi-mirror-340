from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mscope",
    version="0.1.2",
    author="oakwide",
    author_email="mscope@nomail.net",
    description="mscope allows you to find emails by username",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oakwide/mscope",
    packages=find_packages(),
    install_requires=[
        "requests",
        "dnspython"
    ],
    include_package_data=True,
     package_data={
        'mscope': ['*.txt'],
    },
    entry_points={
        "console_scripts": [
            "mscope = mscope.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
