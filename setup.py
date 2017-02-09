from setuptools import setup

requirements = [
    'pyqt5',
    'openpyxl',
    'python-dateutil',
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
    version='0.0.1',
    description="Digest Excel files",
    author="Matthew Lemon",
    author_email='matt@matthewlemon.com',
    url='https://github.com/hammerheadlemon/xldigest',
    packages=['xldigest', 'xldigest.images',
              'xldigest.tests'],
    entry_points={
        'console_scripts': [
            'xldigest-populate = xldigest.database.populate:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='xldigest',
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
