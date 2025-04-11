from setuptools import setup, find_packages

setup(
    name='isoforest_eval',
    version='0.1.0',
    description='A library for evaluating Isolation Forest with linear and logistic regression metrics',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy'
    ],
    python_requires='>=3.7',
)