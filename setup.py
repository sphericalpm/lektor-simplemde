import pathlib

import setuptools


setuptools.setup(
    name='lektor-simplemde',

    use_scm_version=True,
    setup_requires=[
        'setuptools_scm',
    ],

    author='Anton Patrushev',
    author_email='ap@spherical.pm',
    maintainer='spherical.pm',
    maintainer_email='support@spherical.pm',

    description='Plugin integrating SimpleMDE into Lektor admin',
    keywords='Lektor admin plugin simplemde wysiwyg markdown editor',
    license='MIT',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',

    packages=setuptools.find_packages(),
    py_modules=['lektor_simplemde'],

    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
    ],

    extras_require={
        'dev': [
            'spherical-dev[dev]>0.0.2,<0.1',
        ],
    },

    entry_points={
        'lektor.plugins': [
            'simplemde = lektor_simplemde:SimpleMdePlugin',
        ],
    },
)
