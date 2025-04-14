from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='google-map-scraper',
    version='1.0.0',
    description='A fast business scraper for Google Maps using Selenium',  # ✅ Only keep one description
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mukhtar ul Islam',
    author_email='Mukhtarulislam88@hotmail.com',
    url='https://github.com/mukhtar-ul-islam88/google_map_scraper',
    packages=find_packages(),
    install_requires=[
        'selenium==4.31.0',
        'selenium-wire==5.1.0',
        'webdriver-manager==4.0.2',
        'blinker==1.7.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
