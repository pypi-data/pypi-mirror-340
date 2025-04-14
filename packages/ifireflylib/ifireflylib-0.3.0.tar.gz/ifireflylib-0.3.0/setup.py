from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]


setup(
    name="ifireflylib",
    version="0.3.0",
    author="IDSolutions",
    author_email="info@innovativedevsolutions.org",
    description="A client package for Firefly database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitea.innovativedevsolutions.org/IDSolutions/ifireflylib",
    project_urls={
        "Bug Tracker": "https://gitea.innovativedevsolutions.org/IDSolutions/ifireflylib/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={},
    package_data={
        'ifireflylib': ['native/*']
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Topic :: Database",
    ],
    python_requires=">=3.13",
)
