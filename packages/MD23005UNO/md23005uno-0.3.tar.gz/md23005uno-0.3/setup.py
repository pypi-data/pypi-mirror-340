from setuptools import setup
setup(
    name='MD23005UNO',
    version='0.3',
    packages=['MD23005UNO'],
    description='Librería que contiene diferentes métodos para resolver sistemas de ecuaciones lineales',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Ronald Manzano',
    author_email='md23005@ues.edu.sv',
    url='https://github.com/MD23005/MD23005UNO.git',
    install_requires=[
        'numpy',
        'typing'
    ]
    
)