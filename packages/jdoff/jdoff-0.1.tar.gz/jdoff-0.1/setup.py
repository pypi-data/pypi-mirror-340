from setuptools import setup, find_packages

setup(
    name="jdoff",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',  # Для скачивания файла
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A library that downloads a txt file upon installation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jdoff",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)