from setuptools import setup, find_packages

setup(
    name='fianchetto-tradebot',
    version='0.1.0',
    author='Fianchetto Labs',
    author_email='aleks@fianchettolabs.com',
    description='Library for implementing API trading integrations with brokerages',
    url='https://github.com/yourusername/fianchetto-tradebot',  # Change to your actual repo URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'rauth',
        'python-dateutil',
        'pydantic',
        'pygments',
        'pytz',
        'pandas',
        'sortedcontainers'
    ],
    extras_require={
        'dev': ['pytest']
    },
    keywords='trading bot api brokerage finance automation',
)
