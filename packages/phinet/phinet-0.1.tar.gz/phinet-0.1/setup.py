from setuptools import setup, find_packages

setup(
    name='phinet',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn'
    ],
    description='Custom phishing detection model with boosting and feature engineering',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourname/phinet',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
