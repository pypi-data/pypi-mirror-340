from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clipsight",
    version="0.2.0",
    author="duckweeds7",
    author_email="duckweeds7@gmail.com",
    description="A distributed image crawler system with similarity search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duckweeds7/clip-sight",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.68.1",
        "uvicorn>=0.15.0",
        "python-dotenv>=0.19.0",
        "loguru>=0.5.3",
        "playwright>=1.20.0",
        "minio>=7.1.0",
        "redis>=4.0.2",
        "elasticsearch>=7.17.0",
        "celery>=5.2.0",
        "aiohttp>=3.8.1",
        "Pillow>=8.3.1",
        "numpy>=1.21.2",
        "pytest>=6.2.5",
        "pytest-asyncio>=0.16.0",
        "pytest-cov>=2.12.1",
        "black>=21.7b0",
        "isort>=5.9.3",
        "flake8>=3.9.2",
    ],
    entry_points={
        "console_scripts": [
            "clipsight=src.web.app:main",
            "clipsight-worker=src.worker.main:main",
        ],
    },
    license="MIT",
) 