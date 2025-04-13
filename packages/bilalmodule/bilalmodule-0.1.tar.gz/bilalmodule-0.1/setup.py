from setuptools import setup, find_packages

setup(
    name="bilalmodule",  # secretnotes yerine bilalmodule
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pillow',  # PIL için
    ],
    author="Bilal",
    author_email="your.email@example.com",
    description="A secure note-taking module with encryption capabilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bilalmodule",  # URL'yi güncelle
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)