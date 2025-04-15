
from setuptools import setup, find_packages

setup(
    name="orange-postgres-mcp",
    version="0.1.1",
    description="PostgreSQL Tuning and Analysis Tool",
    author="orange",
    author_email="support@orange.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp[cli]>=1.5.0', 'psycopg[binary]>=3.2.6', 'humanize>=4.8.0', 'pglast==7.2.0', 'attrs>=25.3.0', 'psycopg-pool>=3.2.6'],
    keywords=["orange"] + [],
)
