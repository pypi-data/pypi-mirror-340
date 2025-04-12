from setuptools import setup, find_packages

setup(
    name='bilauth',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.3',
    ],
    description='''Bilauth is a Python module that enables programmatic access to Bilfen Lisesi's student portal, offering tools for authentication, data scraping, and structured parsing of profile, exam, and club information. Designed for Bilfen students and developers, Bilauth powers student-only tools, early-stage app testing, and competition-specific access scenarios.''',
    author='Kağan Erkan',
    license='BODL(Custom)',
)
