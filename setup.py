from setuptools import setup, find_packages

setup(
    name="Kit_Big_Data_To_Do_List",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        # liste des dépendances:
        "numpy>=1.18.0",
    ],
    author="Florent BRIAND, Maxime LEDIEU Jaime MONTEA, Edouad DUCLOY, Pierre BILLAUD",
    author_email="florent.briand56@gmail.com",
    description="To Do List helps you manage your agenda by creating a list of your tasks",
    url="https://github.com/jaimeMontea/Kit_BIG_Data",
)
