from setuptools import setup, find_packages

setup(
    name='CodeToClassDiagram',
    version='1.0.2',
    description='Génération de diagrammes de classes à partir d’un projet source.',
    author='Votre Nom',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "regex"
    ],
    entry_points={
        'console_scripts': [
            'code2class=CodeToClassDiagram.main:main',
        ],
    },
)
