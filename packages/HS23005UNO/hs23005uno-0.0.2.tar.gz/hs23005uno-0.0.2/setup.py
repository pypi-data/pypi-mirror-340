from setuptools import setup, find_packages

setup( 
    name='HS23005UNO',
    version='0.0.1',
    description='Libreria para resolver sistemas de ecuaciones lineales y no lineales.',
    author='Noel Alejandro Hernandez Salinas',
    author_email='hs23005@ues.edu.sv',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    entry_points={
        'console_scripts':[
            'hs23005uno=HS23005UNO.main:main'
        ]
    },
    classifiers=[
        'Programming language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6'    
)