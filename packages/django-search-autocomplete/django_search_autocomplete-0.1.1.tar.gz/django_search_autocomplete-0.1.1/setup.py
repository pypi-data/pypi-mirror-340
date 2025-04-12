from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-search-autocomplete",
    version="0.1.1",
    author="islam elmasry",
    author_email="emji555@gmail.com",  # Replace with your email
    description="A flexible Django package for adding search autocomplete functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emji555/django-search-autocomplete",  # Replace with your GitHub repo URL
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Django>=2.2",
    ],
) 