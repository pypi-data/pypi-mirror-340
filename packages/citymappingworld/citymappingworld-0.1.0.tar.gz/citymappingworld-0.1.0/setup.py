from setuptools import setup, find_packages

setup(
    name="citymappingworld",  # <-- updated name
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    description="Returns city options with UTC offset, latitude and longitude from a JSON master list",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ambuj Pratap Jain",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
