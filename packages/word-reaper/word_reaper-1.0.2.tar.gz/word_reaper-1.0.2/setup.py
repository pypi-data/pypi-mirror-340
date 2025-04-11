from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="word-reaper",
    version="1.0.2",
    author="d4rkfl4m3z",
    description="Reap & Forge Wordlists for Password Cracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nemorous/word-reaper",
    project_urls={
        "Documentation": "https://github.com/Nemorous/word-reaper#readme",
        "Bug Tracker": "https://github.com/Nemorous/word-reaper/issues",
        "Source": "https://github.com/Nemorous/word-reaper"
    },
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "wordreaper=word_reaper.word_reaper:main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",  # Or 4 - Beta, 5 - Production/Stable
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Utilities"
    ],
    license="MIT",
    python_requires='>=3.6',
    include_package_data=True,
)

