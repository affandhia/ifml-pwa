import sys
from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)
version = 1.0
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
The usage of this tool require Python {}.{}, but you're trying to
install it on Python {}.{}.
Please use the requested Python version or more to use this tool properly
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

setup(
    name='Django',
    version=version,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://www.djangoproject.com/',
    author='Django Software Foundation',
    author_email='foundation@djangoproject.com',
    description=('A high-level Python Web framework that encourages '
                 'rapid development and clean, pragmatic design.'),
    long_description=read('README.rst'),
    license='BSD',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=['main/bin/itap-cli.py'],
    entry_points={'console_scripts': [
        'django-admin = django.core.management:execute_from_command_line',
    ]},
    install_requires=['pytz'],
    extras_require={
        "bcrypt": ["bcrypt"],
        "argon2": ["argon2-cffi >= 16.1.0"],
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Documentation': 'https://docs.djangoproject.com/',
        'Funding': 'https://www.djangoproject.com/fundraising/',
        'Source': 'https://github.com/django/django',
        'Tracker': 'https://code.djangoproject.com/',
    },
)