# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    
    name='certifyGUI',
    version='0.2.1',
    description='Certificate Designer is a Python GUI tool that lets you visually design and generate personalized certificates from Excel data using a drag-and-drop interface. Built with Tkinter and Pillow, it supports live preview, font customization, and bulk certificate creation with zero coding required.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Muthukumaran S',
    author_email='muthukumarandeveloper@gmail.com',
    url='https://github.com/MuthuKumaran-Dev-10000/certify',
    packages=find_packages(),
    install_requires=[],  # List dependencies here
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
