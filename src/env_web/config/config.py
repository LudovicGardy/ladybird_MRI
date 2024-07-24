import os
from typing import Any

import toml
from dotenv import find_dotenv, load_dotenv


def load_configurations() -> dict[str, Any]:
    """
    Charge uniquement les variables du fichier .env si celui-ci est présent.
    Si le fichier .env n'existe pas, charge toutes les variables d'environnement du système.
    """
    dotenv_path = find_dotenv(".env")

    if dotenv_path:
        # Le fichier .env existe, charger uniquement ses variables
        load_dotenv(dotenv_path)
        # Retourne les variables chargées depuis le .env
        return {
            key: os.environ[key]
            for key in os.environ
            if key in open(dotenv_path).read()
        }
    else:
        # Le fichier .env n'existe pas, retourne toutes les variables d'environnement du système
        return dict(os.environ)


def load_toml_config(file_path) -> dict[str, Any]:
    """
    Charge les configurations à partir d'un fichier .toml
    """
    try:
        with open(file_path, "r") as file:
            return toml.load(file).get("theme", {})
    except FileNotFoundError:
        return {}


def page_config() -> dict[str, Any]:
    """
    Set the page configuration (title, favicon, layout, etc.)
    """
    env_variables = load_configurations()
    toml_config = load_toml_config(".streamlit/config.toml")

    page_dict = {
        "page_title": toml_config.get("page_title", "3D Med Viewer"),
        "sidebar_title": f"# {toml_config.get('sidebar_title', '3D Med Viewer')}",
        "base": toml_config.get("base", "dark"),
        "page_icon": f'{env_variables["AWS_S3_URL"]}/Sotis_AI_pure_darkbg_240px.ico',
        "page_logo": f'{env_variables["AWS_S3_URL"]}/Sotis_AI_pure_darkbg_240px.png',
        "layout": toml_config.get("layout", "centered"),
        "initial_sidebar_state": toml_config.get("initial_sidebar_state", "auto"),
        "author": "Sotis AI",
        "markdown": """
                    <style>
                        .css-10pw50 {
                            visibility:hidden;
                        }
                    </style>
                    """,
        "page_description": """
        This tool is a streamlined and accessible web-based version of a feature from the Ladybird software, as detailed in the [doctoral thesis of L. Gardy, 2021](http://thesesups.ups-tlse.fr/5164/1/2021TOU30190.pdf). 
        \nRedesigned and enhanced in 2024 by L. Gardy, freelance Data Scientist at [Sotis A.I.](https://www.sotisanalytics.com), this tool provides a user-friendly interface for medical image viewing and analysis.
        """,
    }

    return page_dict


def AWS_credentials():
    keys_list = ["AWS_S3_URL"]

    cred_dict = {}
    env_variables = load_configurations()

    # Check if all required keys exist and have a non-empty value
    try:
        for key in keys_list:
            value = env_variables.get(key.upper())
            if not value:
                raise ValueError(f"Missing or empty value for key: {key}")
            cred_dict[key] = value
    except ValueError as e:
        print(f"Configuration error: {e}")
        cred_dict = {}  # Reset cred_dict if any key is missing or empty

    return cred_dict
