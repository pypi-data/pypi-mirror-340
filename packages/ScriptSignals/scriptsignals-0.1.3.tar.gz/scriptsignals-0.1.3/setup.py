from setuptools import setup, find_packages

setup(
    name="ScriptSignals",
    version="0.1.3",
    description="esta libreria te permitira comunicar varios scripts de python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Facundo Efimenco",
    author_email="facu22251@gmail.com",
    url="https://github.com/facu-programer/PySignal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6",
)
