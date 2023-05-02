import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="humanhelp",
    version="0.0.1",
    author="DongHoon Kim",
    author_email="donghoon5793@gmail.com",
    description="Data clustering with human interaction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DongHoon5793/humanhelp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Framework :: Jupyter",
    ],
)