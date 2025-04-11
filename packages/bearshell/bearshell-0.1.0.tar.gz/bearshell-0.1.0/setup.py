from setuptools import setup, find_packages

setup(
    name='bearshell',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A secure shell executor with policy enforcement',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/bearshell',  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
