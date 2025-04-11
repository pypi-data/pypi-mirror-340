from setuptools import setup, find_packages

setup(
    name='bearshell',
    version='0.1.2',
    author='Bradley Reimers',
    author_email='b.a.reimers@gmail.com',
    description='A (relatively) secure and easy-to-use subprocess implementation for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/breimers/bear-shell',  # Replace with your repository URL
    packages=['bearshell'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Topic :: System :: Shells',
    ],
    python_requires='>=3.7',
)
