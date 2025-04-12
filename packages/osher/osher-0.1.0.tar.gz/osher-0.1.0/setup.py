from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="osher",
    version="0.1.0",
    author="OSINT Scout Team",
    author_email="info@osintscout.com",
    description="A comprehensive OSINT (Open Source Intelligence) tool with multiple data sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/osintscout/osher",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Internet",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click",
        "dnspython",
        "email-validator",
        "flask",
        "flask-sqlalchemy",
        "gunicorn",
        "matplotlib",
        "numpy",
        "pandas",
        "phonenumbers",
        "psycopg2-binary",
        "pyopenssl",
        "python-whois",
        "requests",
        "rich",
        "seaborn",
        "whois",
    ],
    entry_points={
        "console_scripts": [
            "osher=osint_scout:cli",
            "osher-web=web_interface:main",
        ],
    },
)