"""
# activar el entorno virtual
ejemplo
PS C:\MSS\AppPython\app_sales> cd ..   
PS C:\MSS\AppPython> cd .\.venv\
PS C:\MSS\AppPython\.venv> cd .\Scripts\
PS C:\MSS\AppPython\.venv\Scripts> .\activate
"""
# isstalar setup tools
#(.venv) PS C:\MSS\AppPython\.venv\Scripts> pip install setuptools

from setuptools import setup,find_packages

setup(
    name='App_sales',
    version='0.1.1',
    author='Frank Muatino Mundaca',
    author_email='fmmundaca@outlook.com',
    description='App para gestionar ventas, precios, impuestos y descuentos',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/FRANKISKAY/Sales_app',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

                ],
    pyhton_requires='>=3.7'     
)
"""
# para poder subir nuestro proyecto en pypip se necesita la herramienta 
#ubicarse en el entorno virtual .venv PIP INTALL TWINE // twine ayuda subir de manera seguro a cualquier repositorio
#luego ir al directorio del proyecto(raiz)
#como subir .. instalar  otras herramientas como  pip install wheel
# crear la distribucion el paquete en formato pip (son,sort,when)
    #debemos estar en el nivel del proyecto
        PS C:\MSS\AppPython\app_sales> "python setup.py sdist bdist_wheel" ///
# en la carpeta dist se encontrara 2 files 
# CERAR UNA CTA EN PYPI.ORG
    SE GENERA UN TOKEN API SE DEBE GUARDAR
    ESTANDO EN LA RAIZ DEL PROYECTO SE DEBE EJECUTAR EL COMANDO
    twine upload dist/*
"""
