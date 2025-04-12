
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vfetch",
    version="0.1.0",
    author="YourName",
    author_email="youremail@example.com",
    description="A beautiful system information display tool with stunning visuals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vfetch",
    packages=find_packages(),
    py_modules=["vfetch", "system_info", "formatters", "themes", "ascii_art"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "psutil>=5.9.0",
        "rich>=12.2.0",
    ],
    entry_points={
        "console_scripts": [
            "vfetch=vfetch:main",
        ],
    },
    include_package_data=True,
    keywords="system-info, fetch, monitoring, cli, terminal, ascii-art",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/vfetch/issues",
        "Source": "https://github.com/yourusername/vfetch",
    },
)
