from setuptools import setup,find_packages

setup(
    name = 'aplicacion_ventas_nicolasort',
    version = '0.1.0',
    author = 'Nicholas Vaca Ortiz',
    author_email = 'nicoalex1718@outlook.com',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url= 'https://github.com/curso_python_camara/gestor/aplicacionventas',
    package= find_packages,
    install_requires=[],
    license='MIT', 
    classifiers=[
        'Programming Language :: Python :: 3', #Cambia esto segun sea necesario
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requieres='>=3,7'
)
