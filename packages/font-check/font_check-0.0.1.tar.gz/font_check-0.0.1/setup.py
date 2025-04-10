from setuptools import setup, find_packages

setup(
    name='font_check',
    version='0.0.1', 
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'font_check': ['data/*.txt'],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='soyvitou',
    author_email='soyvitoupro@gmail.com',
    url='https://github.com/SoyVitouPro/font_check',
    install_requires=[
        "pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
