import os

def get_path():

    path_dict = {
        "toolbar_icones" : os.path.join("src", "env_loval", "static", "toolbar"),
        "mri_examples": os.path.join("src", "env_global", "examples", "mri_examples"),
        "mri.ico": os.path.join("src", "env_local", "static", "mri.ico"),
        "styles.css": os.path.join("src", "env_web", "styles.css"),
    }

    return path_dict
