![task_manager_logo](assets/img/logo.png)

## Project Overview

This project focuses on the development of a __Task Manager__ created as part of the  __Artificial Intelligence__ master's program at  __Telecom Paris__. The main objective of this work is to provide a simple and intuitive application for managing tasks.

## Environment Setup

### Prerequisites

- Python 3.11
- (Optionnel) Poetry pour la gestion des dépendances


### Setup with Poetry

If you have [Poetry](https://python-poetry.org/) installed:

1. **Clone the repository**:
```
   git clone [lien_du_dépôt]
```
```
   cd Kit_BIG_Data
```

2. **Install dependencies**:
```
   poetry install
```

3. **Activate the virtual environment**:
```
   poetry shell
```

### Setup wit Pip

If you are not using Poetry:

1. **Clone the repository**:
```
   git clone [lien_du_dépôt]
```
```
   cd Kit_BIG_Data
```

2. **Create a virtual environment**:
```
python -m venv venv
```

3. **Activate the virtual environment**:
- On Windows :
```
   .\venv\Scripts\activate
```

- On MacOS/Linux:
```
   source venv/bin/activate
```

4. **Install dependencies**:
```
pip install -r requirements.txt
```

### Command Line Interface (CLI)

After setting up the environment:

1. **Navigate to the root project folder (if not already done)**:
```
cd Kit_BIG_Data
```

2. **Launch the CLI**:
```
python -m to_do_list_project.main
```

### Graphical Interface (Streamlit):

After setting up the environment:

1. **Navigate to the root project folder (if not already done)**:
```
cd Kit_BIG_Data
```

2. **Launch the interface**:
```
python -m streamlit run to_do_list_project/streamlit_app.py
```

### Database

SQlite database is used to handle data.
We've chosen this tool in order to demonstrate potentialities with heavier SQL databases and at the same time to remain lightweight.

### CI/CD

GitHub Actions is used for the CI/CD process.
Any push triggers the pipeline, which checks code coverage, linting, docstring and runs tests.

### Documentation Generated with Sphinx:

1. **From the root of the project**:
```
cd docs
```

2. **Generate the documentation**:
```
make html
```

3. Open the file **docs/_build/html/index.html** in your web browser.

### Security

Only official and recognized packages are used into this project.
No environment variables are needed.

### Coding Standards

We follow the [PEP8](https://peps.python.org/pep-0008/) style guide to ensure code clarity and readability.


### Useful Links

- PEP8: [The Style Guide for Python Code](https://peps.python.org/pep-0008/)
- Python: [3.11 Documentation](https://docs.python.org/3.11/)
