from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="judge",
    version="0.1.5",
    description="Lazily review Python project inconsistencies "
    "and vulnerabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BeyonderSolutions/judge",
    author="Rodrigo Gómez Maitret",
    author_email="rodrigo@beyondersolutions.com",
    packages=find_packages(
        include=["judge", "judge.*"]
    ),
    entry_points={
        "console_scripts": [
            "judge = judge:main"
        ]
    },
    install_requires=[
        "rich",
        "toml",
        "flake8==6.1.0",
        "pytest==8.0.0"
    ]
)
