# setup.py
from setuptools import setup, find_packages

setup(
    name='acwa-trainer',
    version='1.0.0',
    author='Huynh Thai Bao',
    author_email='seread335@gmail.com',
    description='Adaptive Class Weight Adjustment (ACWA) for Imbalanced Deep Learning',
    long_description=open('README.md', 'r', encoding='utf-8').read(),  
    long_description_content_type='text/markdown',
    url='https://github.com/Seread335/Thu-t-To-n-Adaptive-Class-Weight-Adjustment-ACWA-.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'torch',
        'torchvision',
        'torchmetrics',
        'numpy',
        'scikit-learn',
        'matplotlib'
    ],
)
