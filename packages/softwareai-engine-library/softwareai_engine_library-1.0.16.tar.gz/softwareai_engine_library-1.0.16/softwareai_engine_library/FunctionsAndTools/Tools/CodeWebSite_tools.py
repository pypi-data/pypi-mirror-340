tools_CodeWebSite = [
    {
        "type": "file_search"
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
            "name": "autoapprovepullrequest",
            "description": "Aprova e mergea o pull request",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_owner": {
                        "type": "string",
                        "description": "Nome do dono do repositorio no GitHub."
                    },
                    "repo_name": {
                        "type": "string",
                        "description":  "Nome do repositório no GitHub."
                    },
                    "pull_number": {
                        "type": "string",
                        "description":  "numero do pull request"
                    },
                    "githubtoken_aprove": {
                        "type": "string",
                        "description": "Token de autenticação do GitHub para realizar operações de aprovar o pull request."
                    },
                    "githubtoken_merge": {
                        "type": "string",
                        "description": "Token de autenticação do GitHub para realizar operações de mergear o pull request."
                    },
                    "approval_message": {
                        "type": "string",
                        "description": "mensagem de aprovacao do pr"
                    },
                    "merge_message": {
                        "type": "string",
                        "description": "mensagem de merge do pr"
                    }
                },
                "required": [
                    "repo_owner",
                    "repo_name",
                    "pull_number",
                    "githubtoken_aprove",
                    "githubtoken_merge",
                    "approval_message",
                    "merge_message"

                    ]
            }
        }
    },               

    {
        "type": "function",
        "function": {
            "name": "autocreateissue",
            "description": "Realiza A criacao de um novo no problema (issue) no repositorio github",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_owner": {
                        "type": "string",
                        "description": "Nome do dono do repositorio no GitHub."
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "Nome do repositório no GitHub."
                    },
                    "issue_title": {
                        "type": "string",
                        "description": "titulo do problema"
                    },
                    "issue_body": {
                        "type": "string",
                        "description": "Descricao do problema"
                    },
                    "githubtoken": {
                        "type": "string",
                        "description": "Token de autenticação do GitHub para realizar operações na API."
                    }
                },
                "required": [
                    "repo_owner",
                    "repo_name",
                    "issue_title",
                    "issue_body",
                    "githubtoken"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "autocreaterepo",
            "description": "Realiza A criacao de um novo repositorio no github",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_owner": {
                        "type": "string",
                        "description": "Nome do dono do repositorio no GitHub."
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "Nome do repositório no GitHub."
                    },
                    "description": {
                        "type": "string",
                        "description": "Descricao de 250 caracteres do projeto."
                    },
                    "githubtoken": {
                        "type": "string",
                        "description": "Token de autenticação do GitHub para realizar operações na API."
                    },
                    "private": {
                        "type": "boolean",
                        "description": "o repositorio deve ser publico com true e privado com false"
                    }
                },
                "required": [
                    "repo_owner",
                    "repo_name",
                    "description",
                    "githubtoken",
                    "private"
                ]
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