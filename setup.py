from setuptools import setup, find_packages

setup(
    name='nextcloud-status',
    version='0.1.0',
    description='A CLI tool for updating NextCloud status',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Colin Jacobs',
    author_email='colin@coljac.net',
    url='https://github.com/coljac/nextcloud-status',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    package_data={'nextcloud_status': ['gh_emoji.json']},
    install_requires=[
        'requests>=2.25.1',
        'typer>=0.12.3'
    ],
    entry_points={
        'console_scripts': [
            'nextcloud-status=nextcloud_status.nextcloud_status:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
