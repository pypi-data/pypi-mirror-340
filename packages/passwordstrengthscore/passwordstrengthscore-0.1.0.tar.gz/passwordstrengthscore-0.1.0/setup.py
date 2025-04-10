from setuptools import setup, find_packages

setup(
    name='passwordstrengthscore',
    version='0.1.0',
    description='A machine learning-based password strength evaluation library',
    author='Encik Megat',
    author_email='muhammed.mazelan03@s.unikl.edu.my',
    url='',  # optional
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'scikit-learn',
        'joblib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
    ],
    python_requires='>=3.7',
)
