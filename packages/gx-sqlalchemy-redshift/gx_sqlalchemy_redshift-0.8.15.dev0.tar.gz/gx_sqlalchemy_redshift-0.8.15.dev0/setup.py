from setuptools import setup

readme = open('README.md').read()
history = open('CHANGES.rst').read().replace('.. :changelog:', '')

setup(
    name='gx-sqlalchemy-redshift',
    version='0.8.15.dev0',
    description='Forked Amazon Redshift Dialect for sqlalchemy',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author='The Great Expectations Team',
    author_email='team@greatexpectations.io',
    license="MIT",
    url='https://github.com/great-expectations/sqlalchemy-redshift',
    packages=['sqlalchemy_redshift', 'redshift_sqlalchemy'],
    package_data={'sqlalchemy_redshift': ['redshift-ca-bundle.crt']},
    python_requires='>=3.4',
    install_requires=[
        'SQLAlchemy>2.0.7',
        'packaging',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'redshift = sqlalchemy_redshift.dialect:RedshiftDialect_psycopg2',
            'redshift.psycopg2 = sqlalchemy_redshift.dialect:RedshiftDialect_psycopg2',
            'redshift.psycopg2cffi = sqlalchemy_redshift.dialect:RedshiftDialect_psycopg2cffi',
            'redshift.redshift_connector = sqlalchemy_redshift.dialect:RedshiftDialect_redshift_connector',
        ]
    },
)
