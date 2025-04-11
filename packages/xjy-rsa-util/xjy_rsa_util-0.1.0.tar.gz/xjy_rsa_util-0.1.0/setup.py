from setuptools import setup, find_packages

setup(
    name="xjy_rsa_util",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'cryptography>=3.4',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A utility for RSA signing and request body building",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/xjy_rsa_util",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)