import os

def get_path():

    root = os.getcwd()

    path_dict = {

        "root" : root,
        "toolbar_icones" : os.path.join(root, "ladybird_MRI_app", "static", "toolbar"),
        "mri_examples": os.path.join(root, "ladybird_MRI_app", "static", "mri_examples")
    }

    return path_dict
