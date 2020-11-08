from os.path import dirname
from os.path import join
from setuptools import setup


def read_file(fname):
    "Read a local file"
    return open(join(dirname(__file__), fname)).read()


setup(
    name='mkdocs-codeinclude-plugin',
    version_config={
        "version_format": "{tag}.dev{sha}",
        "starting_version": "0.2.0"
    },
    description="A plugin to include code snippets into mkdocs pages",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown codeinclude',
    url='https://github.com/rnorth/mkdocs-codeinclude-plugin',
    author='Richard North',
    author_email='rich.north@gmail.com',
    license='MIT',
    python_requires='>=3.7',
    install_requires=[
        'mkdocs>=0.17',
        'pygments'
    ],
    setup_requires=['better-setuptools-git-version'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['codeinclude'],
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'codeinclude = codeinclude.plugin:CodeIncludePlugin'
        ]
    }
)
