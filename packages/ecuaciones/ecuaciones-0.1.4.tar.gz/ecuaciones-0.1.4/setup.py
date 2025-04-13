from setuptools import setup, find_packages

setup(
    name='ecuaciones',
    version='0.1.4',
    packages=find_packages(),  
    install_requires=[
        'numpy',  
    ],
    include_package_data=True,  
    license='MIT',  
    description='Librería para resolver sistemas de ecuaciones',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/tu_repositorio',
    author='Tu Nombre',
    author_email='tu_correo@example.com',
)
