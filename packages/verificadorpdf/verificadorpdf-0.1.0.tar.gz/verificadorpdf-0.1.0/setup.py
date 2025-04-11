from setuptools import setup, find_packages

setup(
    name='verificadorpdf',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'PyPDF2'
    ],
    author='Helio Carmo',
    author_email='helio.h.carmo@gmail.com',
    description='Um pacote para verificar palavras dentro de arquivos PDF',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Helio-Carmo/verificador-de-palavra-pdf.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)