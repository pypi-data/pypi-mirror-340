from setuptools import setup, find_packages

setup(
    name='word-reaper',
    version='1.0.0',
    author='d4rkfl4m3z',
    description='Extract & Forge Wordlists for Password Cracking',
    packages=find_packages(),
    install_requires=[
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'wordreaper=word_reaper.word_reaper:main'
        ]
    },
    include_package_data=True,
    python_requires='>=3.6',
)

