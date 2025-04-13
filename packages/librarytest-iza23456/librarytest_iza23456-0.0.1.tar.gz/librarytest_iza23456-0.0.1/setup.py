from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name='librarytest_iza23456',
    version='0.0.1',
    description='A short summary about your package',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='iza',
    author_email='isai.arh18@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='test',
    packages=['test-lib'],
    install_requires=['']
)