from setuptools import setup, find_namespace_packages

# Try to read the README.md file from the correct location
try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    # Fallback to a simple description if README.md is not found
    long_description = "A client package for FireFlyDB"

setup(
    name="ifireflylib",
    version="0.0.1",
    description="A client package for FireFlyDB",
    author="IDSolutions",
    packages=find_namespace_packages(include=["ifireflylib", "ifireflylib.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitea.innovativedevsolutions.org/IDSolutions/firefly",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.13",
    package_data={
        'ifireflylib': [
            'native/libFireflyClient.dll',
            'native/libFireflyClient.so',
            'native/libFireflyClient.dylib'
        ]
    },
    include_package_data=True,
)
