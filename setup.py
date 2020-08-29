import setuptools
from distutils.core import setup

setup(
    name='telisar',
    version='1.0.3',
    description='D&D tomfoolery for the Telisar campaign setting',
    classifiers=[
    ],
    keywords='',
    url='',
    author='evilchili',
    author_email='evilchili@gmail.com',
    license='Unlicense',
    packages=setuptools.find_packages(),
    package_dir={'telisar': 'telisar'},
    include_package_data=True,
    zip_safe=False,
    data_files=[
        ('telisar', [
            'data/LICENSE_THINGS_database.txt',
            'data/LICENSE_WordNet.txt',
            'data/adjectives',
            'data/nouns'
        ]),
    ],
    entry_points={
        'console_scripts': [
            'calendar=telisar.cli:calendar'
            'timeline=telisar.cli:timeline'
            'hoard=telisar.cli:hoard'
            'npc=telisar.cli:npc'
            'text=telisar.cli:text'
            'bot=telisar.cli:bot'
        ],
    }
)
