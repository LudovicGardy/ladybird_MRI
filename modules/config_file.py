import os

def get_path():

    root = os.getcwd()

    path_dict = {

        "root" : root,
        "toolbar_icones" : os.path.join(root, "modules", "static", "toolbar"),
        "mri_examples": os.path.join(root, "modules", "static", "mri_examples")
    }

    return path_dict
