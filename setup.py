from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Profil Reviewer',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
]

setup(
    name='ProfilLogger',
    version='0.0.1',
    description='Basic logger',
    long_description=open('README.txt').read(),
    url='',
    author='Jakub Podolski',
    author_email='jakub.m.podolski@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='logging',
    packages=find_packages(),
    install_requires=['']
)