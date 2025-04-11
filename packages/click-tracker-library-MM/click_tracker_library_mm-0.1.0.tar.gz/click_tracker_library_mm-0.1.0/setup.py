# setup.py

from setuptools import setup, find_packages

setup(
    name='click_tracker_library_MM',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.0.0',
        'requests',
        'user-agents',
    ],
    author='M_MOHAMED',
    author_email='mohamedmeksi37@gmail.com',
    description='A reusable Flask library for tracking clicks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MohamedMeksi/click_tracker_library_MM',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)