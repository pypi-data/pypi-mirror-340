from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "click>=8.1.3,<9.0.0",
    "inquirer>=3.1.3,<4.0.0",
    "jinja2>=3.1.2,<4.0.0",
    "pydantic>=2.0.0,<3.0.0",
    "talos-aclient==1.6.0",
]

setup(
    name="talos-loader",
    version="0.0.3",
    description="A tool for creating and managing loader projects",
    author="Your Name",
    author_email="your.email@example.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,  # 确保包含MANIFEST.in中指定的文件
    package_data={
        "talos_loader": ["templates/*.j2", "templates/*.py", "templates/__init__.py"],
    },
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "talos-loader=talos_loader.cli:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
