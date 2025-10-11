from setuptools import setup, find_packages

setup(
    name="issueping",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "requests>=2.32.0",
        "sendgrid>=6.11.0",
    ],
    entry_points={
        "console_scripts": [
            "issueping=issueping.main:main",
        ],
    },
)
