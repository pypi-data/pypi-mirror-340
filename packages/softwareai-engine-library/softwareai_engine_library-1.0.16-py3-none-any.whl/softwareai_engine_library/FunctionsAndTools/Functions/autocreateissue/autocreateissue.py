#########################################
# IMPORT SoftwareAI Libs 
from CoreEngine.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from CoreEngine.Inicializer._init_core_ import *
#########################################


def autocreateissue(
                repo_owner: str,
                repo_name: str,
                issue_title: str,
                issue_body: str,
                githubtoken: str
                ):
    issue_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"token {githubtoken}",
        "Accept": "application/vnd.github.v3+json"
    }
    issue_data = {
        "title": issue_title,
        "body": issue_body
    }
    
    response = requests.post(issue_url, json=issue_data, headers=headers)
    
    if response.status_code == 201:
        print(f"Issue '{issue_title}' criada com sucesso no repositório {repo_name}")
        return {"status": "success", "message": f"Issue '{issue_title}' criada com sucesso"}
    else:
        print(f"Falha ao criar a issue. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}






