import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

#información de contacto de los autores
AUTHORS = [ 
    { "name": "@greenmay", "email": "maydaymm66@yahoo.com" }, 
    { "name": "@juan", "email": "juan@example.com" }
]
author_names = ", ".join(author["name"] for author in AUTHORS)
author_emails = ", ".join(author["email"] for author in AUTHORS)

setuptools.setup (
    name = 'SMVLibreria',  #para el import
    version ='1.0.0', #se va cambiando según se incluyan cambios
    description = 'Libreria para sumar dos números',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = author_names,
    author_email = author_emails,
    url = 'https://github.com/greenmay99/semovi_libreria',
    license = "MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10"
)