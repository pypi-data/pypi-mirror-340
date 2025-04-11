from setuptools import setup, find_packages

setup(
    name="cloudstaffsync_utils",
    version="0.1.0",
    description="Utility package for cloudstaffsync",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/Kotapavankalyanreddy/cloud_utils",
    packages=find_packages(),  # Will include dietlytic_utils and utils
    python_requires=">=3.6",
)
