from setuptools import setup, find_packages

setup(
    name="at-client-data",
    version="0.2.3",
    description="AT Client and Schema Package for AT Data API",
    author="Ray",
    author_email="rayanywhere@gmail.com",
    url="https://github.com/apex-trader/at-backend-data",
    packages=find_packages(include=['at_client_data', 'at_client_data.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=1.8.0",
    ],
) 