from setuptools import setup, find_packages

setup(
    name="mp4mdl",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "requests",
        "urllib3",
        "beautifulsoup4",
        "ffmpeg-python",
    ],
    author="Maddox",
    author_email="maddoxtes@gmail.com",
    description="Un outil pour télécharger et gérer des vidéos MP4",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://git.maddoxserv.com/maddox/MP4MDL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "mp4mdl=mp4mdl.main:main",
        ],
    },
)
