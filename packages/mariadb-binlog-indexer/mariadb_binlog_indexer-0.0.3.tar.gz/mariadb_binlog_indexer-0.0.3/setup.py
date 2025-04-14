from setuptools import setup

setup(
    name="mariadb_binlog_indexer",
    version="0.0.3",
    description="MariaDB Binlog Indexer for Faster Querying",
    long_description=open("README.md").read(),  # noqa: SIM115
    long_description_content_type="text/markdown",
    packages=["mariadb_binlog_indexer"],
    package_data={
        "mariadb_binlog_indexer": ["lib/indexer*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.10",
    install_requires=["duckdb==1.2.2"],
)
