tools_CodeDocumentation = [
    {
        "type": "file_search"
    },
    {
        "type": "function",
        "function": {
            "name": "autosave",
            "description": "Salva um codigo python em um caminho",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "codigo"
                    },
                    "path": {
                        "type": "string",
                        "description": "Caminho do codigo"
                    }
                },
                "required": ["code","path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_to_webhook_func",
            "description": "Envia uma menssagem para um usuario em expecifico do webhook",
            "parameters": {
                "type": "object",
                "properties": {
                    "user": {
                        "type": "string",
                        "description": "user to message"
                    },
                    "type": {
                        "type": "string",
                        "description": "type e.g 'info' "
                    },
                    "message": {
                        "type": "string",
                        "description": "message "
                    },
                    "cor": {
                        "type": "string",
                        "description": "cor e.g blue "
                    }
                },
                "required": ["user","type", "message", "cor"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "autopullrequest",
            "description": "cria um novo pull request no repositorio GitHub.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_owner": {
                        "type": "string",
                        "description": "Nome do dono do repositorio no GitHub."
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "Nome do repositorio no GitHub."
                    },
                    "branch_name": {
                        "type": "string",
                        "description": "Nome da branch onde o codigo ser atualizado."
                    },
                    "file_paths": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Lista de caminhos dos arquivos no repositório."
                    },
                    "commit_message": {
                        "type": "string",
                        "description": "Mensagem de commit descrevendo as melhorias."
                    },
                    "improvements": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Lista de melhorias no código."
                    },
                    "pr_title": {
                        "type": "string",
                        "description": "Titulo do Pull request."
                    },
                    "github_token": {
                        "type": "string",
                        "description": "Token de autentica\u00e7\u00e3o do GitHub."
                    }
                },
                "required": [
                    "repo_owner",
                    "repo_name",
                    "branch_name",
                    "file_paths",
                    "commit_message",
                    "improvements",
                    "pr_title",
                    "github_token"
                ]
            }
        }
    }

]