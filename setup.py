from setuptools import setup

requirements = [
    'pyqt5', 'openpyxl', 'python-dateutil', 'sqlalchemy', 'appdirs', 'Mako'
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-faulthandler',
    'pytest-mock',
    'pytest-qt',
    'pytest-xvfb',
]

setup(
    name='xldigest',
    version='0.2',
    description="Digest Excel files",
    long_description="Digest Excel files",
    author="Matthew Lemon",
    author_email='matt@matthewlemon.com',
    url='https://github.com/hammerheadlemon/xldigest',
    packages=[
        'xldigest', 'xldigest.process', 'xldigest.process',
        'xldigest.database', 'xldigest.widgets', 'xldigest.analysis',
        'xldigest.tests'
    ],
    py_modules=['icons_rc'],
    entry_points={
        'console_scripts':
        ['xldigest-populate = xldigest.database.populate:main']
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='Excel, spreadsheet, collection, database, analysis',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    license='MIT'
)
