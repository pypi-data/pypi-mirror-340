from setuptools import setup, find_packages

setup(
    name="webengage-migration",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "we=historical_data_migration.migration:main",
        ],
    },
    author="Nipun Patel",
    author_email="nipunp27@gmail.com",
    description="Webengage internal tool to migrate other party historical data into webengage ecosystem",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://www.webengage.com/",
    license="MIT",
    license_files=["LICEN[CS]E.*"], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
