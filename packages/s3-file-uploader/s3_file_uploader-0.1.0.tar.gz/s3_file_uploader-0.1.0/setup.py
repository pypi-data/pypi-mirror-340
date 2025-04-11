from setuptools import setup, find_packages

setup(
    name="s3-file-uploader",
    version="0.1.0",
    description="A flexible and dynamic file uploader for S3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Md Anisur Rahman",
    author_email="anisurrahman14046@gmail.com",
    # url="https://github.com/yourusername/file-uploader",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
