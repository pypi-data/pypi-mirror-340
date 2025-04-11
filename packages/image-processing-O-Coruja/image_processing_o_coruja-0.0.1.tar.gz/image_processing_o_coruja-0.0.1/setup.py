from setuptools import setup, find_packages

with open ("README.md", "r") as f:
    page_description = f.read()

with open ("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(

    name="image_processing_O_Coruja",
    version="0.0.1",
    author="Rodrigo_Cazelli",
    author_email="rcazelli@yahoo.com.br",
    description="",
    long_description="",
    long_description_content_type="",
    url="",
    packages=find_packages(),
    install_requires="",
    python_requires =">=3.8",
)

