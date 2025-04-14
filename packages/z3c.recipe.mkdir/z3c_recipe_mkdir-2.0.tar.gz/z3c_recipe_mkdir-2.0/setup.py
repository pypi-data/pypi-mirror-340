import os

from setuptools import setup


version = '2.0'

with open("README.rst") as f:
    README = f.read()

with open(os.path.join("src", "z3c", "recipe", "mkdir", "README.rst")) as f:
    DETAILED = f.read()

with open("CHANGES.rst") as f:
    CHANGES = f.read()


setup(
    name='z3c.recipe.mkdir',
    version=version,
    description="Buildout recipe to create directories.",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Buildout",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Zope Public License",
    ],
    keywords='buildout directory folder mkdir',
    author='Uli Fouquet',
    author_email='grok-dev@zope.org',
    url='https://github.com/zopefoundation/z3c.recipe.mkdir',
    license='ZPL-2.1',
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
        'zc.buildout >= 1.5',
    ],
    extras_require={
        'test': [
            'zope.testing',
            'zope.testrunner >= 6.4',
        ],
        'testing': [
            'zope.testing',
            'zope.testrunner >= 6.4',
        ],
        'docs': ['Sphinx'],
    },
    entry_points="""
      [zc.buildout]
      default = z3c.recipe.mkdir:Recipe
      """,
)
