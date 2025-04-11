from setuptools import setup, find_packages

setup(
    name='django-hey',
    version='0.1.9',  # Incremented to force reinstall
    packages=find_packages(),
    install_requires=[
        'django>=3.0',
    ],
    author='Sabari Nathan',
    author_email='sabareee000@gmail.com',
    description='A Django command to create a project and app with a single command',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sabari7497/django-hey',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'hey=django_hey.hey:main',
        ],
    },
)