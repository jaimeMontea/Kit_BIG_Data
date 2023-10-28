![task_manager_logo](https://github.com/jaimeMontea/Kit_BIG_Data/assets/45881846/b91f92a6-266d-433c-a075-cdb86ebf13ba)

## Présentation du Projet

Ce projet porte sur la réalisation d'un __Task Manager__ réalisée dans le cadre du mastère __Intelligence Artificielle__ de Telecom Paris. Le principal objectif de ce travail est d'offrir une application simple et intuitive pour gérer des tâches.

## Configuration de l'environnement

### Pré-requis

- Python 3.11
- (Optionnel) Poetry pour la gestion des dépendances


### Mise en place avec Poetry

Si vous avez [Poetry](https://python-poetry.org/) installé :

1. **Clonez le dépôt**:
```
   git clone [lien_du_dépôt]
```
```
   cd Kit_BIG_Data
```

2. **Installez les dépendances**:
```
   poetry install
```

3. **Activez l'environnement virtuel**:
```
   poetry shell
```

### Mise en place sans Poetry

Si vous n'utilisez pas Poetry :

1. **Clonez le dépôt**:
```
   git clone [lien_du_dépôt]
```
```
   cd Kit_BIG_Data
```

2. **Créez un environnement virtuel**:
```
python -m venv venv
```

3. **Activez l'environnement virtuel**:
- Sur Windows :
```
   .\venv\Scripts\activate
```

- Sur MacOS/Linux:
```
   source venv/bin/activate
```

4. **Installez les dépendances**:
```
pip install -r requirements.txt
```

### Lancement du projet

Après avoir configuré l'environnement :

1. **Naviguez vers le dossier du projet (si ce n'est déjà fait)**:
```
cd Kit_BIG_Data
```

2. **Lancez le projet**:
```
python -m to_do_list_project.main
```

### Documentation générée avec Sphinx :

1. **Depuis la racine du projet**:
```
cd docs
```

2. **Générer la documentation**:
```
make html
```

3. Ouvrez le fichier docs/_build/html/index.html sur votre navigateur internet.

### Ouvrir l'interface graphique générée avec Streamlit :

1. **Depuis la racine de votre projet**:
```
python -m streamlit run to_do_list_project/streamlit_app.py
```
### Normes de codage

Nous suivons le guide de style [PEP8](https://peps.python.org/pep-0008/) pour assurer la clarté et la lisibilité du code.


### Liens utiles

- PEP8: [Guide de style pour le code Python](https://peps.python.org/pep-0008/)
- Python: [Documentation 3.11](https://docs.python.org/3.11/)
