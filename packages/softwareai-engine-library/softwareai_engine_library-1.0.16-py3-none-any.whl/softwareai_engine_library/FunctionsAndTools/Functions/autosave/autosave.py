#########################################
# IMPORT SoftwareAI Libs 
from CoreEngine.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from CoreEngine.Inicializer._init_core_ import *
#########################################


def autosave(code, path):
    """
    Save the provided Python code string to a file.

    Parameters:
    ----------
    code (str): The Python code to save.
    path (str): The name of the file where the code will be saved.

    Returns:
    -------
    None
    """
    try:
        with open(path, 'w', encoding="utf-8") as file:
            file.write(code)
        return {"status": "success", "message": "True"}
    except Exception as e:
        print(e)
        with open(path, 'x', encoding="utf-8") as file:
            file.write(code)
        return {"status": "success", "message": "True"}