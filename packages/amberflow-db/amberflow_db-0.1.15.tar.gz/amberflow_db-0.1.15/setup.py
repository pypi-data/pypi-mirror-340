from setuptools import setup, find_packages

setup(
    name="amberflow-db",
    packages=find_packages(
        include=["amberflow_db", "amberflow_db.*"]
    ),  # This will include all subpackages
    version="0.1.15",
    author="AmberFlow",
    description="The database for AmberFlow",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
    ],
)
