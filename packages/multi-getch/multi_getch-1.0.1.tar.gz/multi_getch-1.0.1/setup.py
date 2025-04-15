from setuptools import find_packages, setup

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='multi-getch',
    version='1.0.1',
    description='multiplatform getch',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='azzammuhyala',
    author_email='azzammuhyala@gmail.com',
    license='MIT',
    python_requires='>=3.0',
    packages=find_packages(),
    include_package_data=True,
    keywords=['getch', 'multiplatform getch', 'simple getch', 'get character'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)