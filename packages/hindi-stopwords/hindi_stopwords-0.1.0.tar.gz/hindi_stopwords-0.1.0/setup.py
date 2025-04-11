from setuptools import setup, find_packages

setup(
    name='hindi_stopwords',
    version='0.1.0',
    description='A Hindi stopword removal library for Python',
    author='IND-WSDpro',
    author_email='deepankargupta874@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Natural Language :: Hindi',
    ],
    python_requires='>=3.6',
)
