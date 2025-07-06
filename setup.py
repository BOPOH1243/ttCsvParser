from setuptools import setup, find_packages

setup(
    name="csv_processor",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "csv_processor = csv_processor:main"
        ]
    },
    install_requires=[
        "tabulate"
    ],
)