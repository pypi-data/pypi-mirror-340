from setuptools import setup, find_packages

setup(
    name='linear-nonlinear-solver',
    version='0.1.0',
    author='Tu Nombre',
    author_email='tu.email@example.com',
    description='Una librería para resolver sistemas de ecuaciones lineales y no lineales.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/linear-nonlinear-solver',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)