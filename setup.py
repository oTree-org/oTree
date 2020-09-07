import os
import sys
from setuptools import setup, find_packages
import shutil
from pathlib import Path

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

import otree
version = otree.__version__

with open('README.rst', encoding='utf-8') as f:
    README = f.read()

with open('requirements.txt', encoding='utf-8') as f:
    required = f.read().splitlines()

with open('requirements_mturk.txt', encoding='utf-8') as f:
    required_mturk = f.read().splitlines()


if sys.argv[-1] == 'publish':

    if Path('dist').is_dir():
        shutil.rmtree('dist')
    for cmd in [
        "python setup.py sdist",
        "twine upload dist/*",
        f'git tag -a {version} -m "version {version}"',
        "git push --tags"
    ]:
        sys.stdout.write(cmd + '\n')
        exit_code = os.system(cmd)
        if exit_code != 0:
            raise AssertionError

    sys.exit()

# 3.7 because of hypercorn

MSG_PY_VERSION = f"""
Error: This version of oTree requires Python 3.7 or higher.

If you're seeing this message on oTree Hub, 
upgrade oTree locally and run "otree zip" again.

If using Heroku without oTree Hub, you should create a runtime.txt 
as described in the Heroku documentation.
"""

if sys.version_info < (3, 7):
    sys.exit(MSG_PY_VERSION)


setup(
    name='otree',
    version=version,
    include_package_data=True,
    license='MIT License',
    # 2017-10-03: find_packages function works correctly, but tests
    # are still being included in the package.
    # not sure why. so instead i use
    # recursive-exclude in MANIFEST.in.
    packages=find_packages(),
    description=(
        'oTree is a toolset that makes it easy to create and '
        'administer web-based social science experiments.'
    ),
    long_description=README,
    url='http://otree.org/',
    author='chris@otree.org',
    author_email='chris@otree.org',
    install_requires=required,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        # example license
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    entry_points={
        'console_scripts': [
            'otree=otree_startup:execute_from_command_line',
        ],
    },
    zip_safe=False,
    extras_require={
        'mturk': required_mturk
    }
)
