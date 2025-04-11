# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kmr1-shorten",
    version="1.0.2",
    packages=["kmr1_shorten"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "kmr1-shorten = kmr1_shorten.shorten:main",
            "k1s = kmr1_shorten.shorten:main",
        ]
    },
    author="Lapius7bot Technology Co.",
    author_email="contact-us@lapius7.com",
    description="Kmr¹ APIを使用してURLを短縮するコマンドラインツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
)