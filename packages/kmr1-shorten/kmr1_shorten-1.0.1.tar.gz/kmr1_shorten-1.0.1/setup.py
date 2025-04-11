# setup.py
from setuptools import setup, find_packages

setup(
    name="kmr1-shorten",
    version="1.0.1",
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
    description="Kmr¹ APIを使用してURLを短縮するコマンドライン",
    url="https://api.kmr1.org/v1/use",
    license="MIT",
    package_data={
        "": ["LICENSE"],
    },
    include_package_data=True,
)