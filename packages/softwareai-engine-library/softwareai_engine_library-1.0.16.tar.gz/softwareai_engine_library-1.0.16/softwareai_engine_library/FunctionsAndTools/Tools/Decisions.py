tools_Decisions = [
    {
        "type": "file_search"
    },
    {
        "type": "function",
        "function": {
            "name": "criar_grafico",
            "description": "Cria gráficos de linha, barra ou pizza.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tipo": {
                        "type": "string",
                        "description": "tipo (str): Tipo de gráfico ('linha', 'barra', 'pizza')."
                    },
                    "dados": {
                        "type": "object",
                        "description": "Para 'linha' e 'barra', use {'x': [...], 'y': [...]}. Para 'pizza', use {'labels': [...], 'valores': [...]}",
                        "properties": {
                            "x": {
                            "type": "array",
                            "items": { "type": "string" },
                            "description": "Valores do eixo X (ex: ['Jan', 'Fev', 'Mar'])"
                            },
                            "y": {
                            "type": "array",
                            "items": { "type": "number" },
                            "description": "Valores do eixo Y (ex: [100, 200, 150])"
                            }
                    },
                    "required": []
                    },
                    "titulo": {
                        "type": "string",
                        "description": "Título do gráfico "
                    },
                    "xlabel": {
                        "type": "string",
                        "description": " Rótulo do eixo X (para linha/barra)."
                    },
                    "ylabel": {
                        "type": "string",
                        "description": "Rótulo do eixo Y (para linha/barra)."
                    },
                    "salvar_em": {
                        "type": "string",
                        "description": " Caminho do arquivo para salvar (ex: 'grafico.png'). Se None, exibe o gráfico."
                    }
                    
                },
                "required": ["tipo",
                            "dados", 
                            "titulo", 
                            "xlabel", 
                            "ylabel", 
                            "salvar_em"
                        ]
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
    

]