# AI Module Destination Explorer

## Overview
This is the project to implement the AI Model using pretrained model Word2Vec. We also provide the tutorial for setting up the environment.

## Requirements
Please install these:
- Python 3.x
- pip (Python package installer)

## Steps to Run the Project

### 1. Creating a Virtual Environment

Create a virtual environment for this project to isolate dependencies from your main Python system.

```sh
python -m venv venv
```

### 2. Activating the Virtual Environment

Activate the virtual environment that has been created. This step differs depending on the operating system you are using.

#### For Windows:
```sh
cd venv\Scripts
.\activate
```

#### For MacOS/Linux:
```sh
source venv/bin/activate
```

### 3. Installing Required Packages

Once the virtual environment is activated, install all required packages using `requirements.txt`.

```sh
pip install -r requirements.txt
```

### 4. Returning to the Project Directory

Ensure you are in the project directory before running the Flask server.

```sh
cd ../..  # Repeat as necessary to return to the project directory
```

### 5. Running the Project

Run the Flask server to start the application.

```sh
python -m flask run
```

The Flask server will run at `http://127.0.0.1:5000`.

## Notes

- Ensure you have created a `requirements.txt` file that contains all project dependencies.
- If you are using Flask environment variables (such as `FLASK_APP`), make sure to set them before running the project.
