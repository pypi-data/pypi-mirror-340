from setuptools import setup, find_packages

setup(
    name='GA22038UNO',
    version='0.1.0',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales',
    author='Tu Nombre',
    author_email='tu_email@example.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
