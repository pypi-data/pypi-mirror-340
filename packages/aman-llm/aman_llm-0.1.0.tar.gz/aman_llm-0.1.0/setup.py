from setuptools import setup, find_packages

setup(
    name='aman_llm',
    version='0.1.0',
    author='Aman Prasad',
    author_email='amanprasad5455@gmail.com',
    description='this will integrate ai power in your code',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/amanprasadoo7/my-pip.git',
    packages=find_packages(),
    install_requires=[
        'agno',
        'google-genai',
        'python-dotenv',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
