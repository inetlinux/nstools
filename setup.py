import setuptools
import nstools

classifiers = [
    'Environment :: Console',
    'License :: OSI Approved :: BSD License',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Security',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
    'Topic :: System :: Networking',
    'Topic :: System :: Shells',
    'Topic :: Utilities',
]

setuptools.setup(
    name='nstools',
    version=nstools.version,
    summary = 'Tools for learning network protocol',
    author = 'Inetlinux',
    author_email = 'lijing@inetlinux.com',
    url = 'http://github.io/inetlinux/nstools',
    scripts=['bin/ns'],
    packages=['nstools', 'nstools.cmd', 'nstools.plugins'],
    platforms = 'OS Independent',
    license='BSD License',
    classifiers=classifiers,
)
