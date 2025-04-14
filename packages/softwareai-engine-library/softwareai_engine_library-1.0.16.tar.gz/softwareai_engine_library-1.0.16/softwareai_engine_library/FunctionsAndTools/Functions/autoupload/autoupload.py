#########################################
# IMPORT SoftwareAI Libs 
from CoreEngine.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from CoreEngine.Inicializer._init_core_ import *
#########################################


def get_file_sha(repo, path, token):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

def autoupload(
                softwarepypath: str,
                repo_name: str,
                token: str
            ):
    

    
    directory = os.path.dirname(softwarepypath)

    with open(softwarepypath, "rb") as file:
        content = file.read()
        encoded_content = base64.b64encode(content).decode("utf-8")

    relative_path = os.path.relpath(softwarepypath, start=directory)  
    filename = os.path.basename(softwarepypath)
    github_path = relative_path.replace("\\", "/")  

    url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/contents/{github_path}"

    response = requests.get(url, headers={"Authorization": f"token {token}"})
    sha = response.json().get("sha") if response.status_code == 200 else None

    data = {
        "message": f"Update {filename}",
        "content": encoded_content,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha 

    put_response = requests.put(url, json=data, headers={"Authorization": f"token {token}"})
    if put_response.status_code in (200, 201):
        return {"status": "success", "message": f"Arquivo: {github_path} - Status: Sucesso ({put_response.status_code})"}
    else:
        return {"status": "success", "message": f"Erro ao enviar {github_path}: Status {put_response.status_code} - {put_response.text}"}

    

