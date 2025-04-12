from setuptools import setup, find_packages

setup(
    name="zekai_utils",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'torch',
        'numpy',          
        'Pillow',         
        'opencv-python',  
        'imageio',
        'safetensors',
        'loguru',
        'tqdm',
        'colorama',
    ],
    author="Zekai Zhang",
    author_email="justinzzk2002@163.com",
    description="Zekai's python utils",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="",
    classifiers=[
        'License :: OSI Approved :: Academic Free License (AFL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)