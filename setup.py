import os
from setuptools import setup, find_packages


def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mkdocs-codeinclude-plugin',
    version='0.0.1',
    description="TODO",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown codeinclude',
    url='TODO',
    author='Richard North',
    author_email='TODO',
    license='Apache-2.0',
    python_requires='>=3.6',
    install_requires=[
        'mkdocs>=0.17',
        'mkdocs'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': [
            'codeinclude = codeinclude.plugin:CodeIncludePlugin'
        ]
    }
)