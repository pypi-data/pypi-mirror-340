from setuptools import setup, find_packages

setup(
    name="db-shifter",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
    ],
    entry_points={
        "console_scripts": [
            "db-shifter=db_shifter.__main__:main"
        ]
    },
    author="Your Real Name or Alias",
    author_email="you@example.com",
    description="A toxic lil' tool to sync missing rows between two Postgres DBs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/goodness5/db-shifter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
