from setuptools import setup, find_packages

setup(
    name="language_core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.0',
        'nltk>=3.8.1',
        'tqdm>=4.65.0',
        'PyYAML>=6.0.0',
        'pytest>=7.0.0'
    ],
    author="AI Language Generator Team",
    description="A system for generating artificial languages",
    python_requires='>=3.8',
)
