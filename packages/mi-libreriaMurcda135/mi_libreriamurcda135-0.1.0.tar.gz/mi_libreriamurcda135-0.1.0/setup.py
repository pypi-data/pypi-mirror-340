from setuptools import setup, find_packages

setup(
    name='mi_libreriaMurcda135',
    version='0.1.0',
    description='Librería educativa para métodos de sistemas de ecuaciones lineales y no lineales',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Marcos Murga',
    author_email='mm22090@ues.edu.sv',
    url='https://github.com/Marsharmurg/mi_libreria',  # Cambiar si tienes un repo
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Education',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy'
    ],
)
