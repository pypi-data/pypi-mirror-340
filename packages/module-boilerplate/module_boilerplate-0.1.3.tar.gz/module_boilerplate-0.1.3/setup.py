from setuptools import setup, find_packages

setup(
    name='module_boilerplate',
    version='0.1.3', 
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'rdlab_dataset': ['data/*.pkl', 'font/*.ttf'],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='soyvitou',
    author_email='soyvitoupro@gmail.com',
    url='https://github.com/SoyVitouPro/python-modules-boilerplate',
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
