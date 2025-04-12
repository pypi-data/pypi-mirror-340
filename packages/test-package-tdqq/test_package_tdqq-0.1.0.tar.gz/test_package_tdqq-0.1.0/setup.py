from setuptools import setup, find_packages

setup(
    name="test_package_tdqq",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas"],
    author="Thuong Dang, Qiqi Chen",
    author_email="dangtuanthuong@gmail.com",
    description="Simple test package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",
    license_files=['LICENSE'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
