tools_NextReviewer = [
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
            "name": "autoconversationissue",
            "description": "responde ao usuario no pull request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Dono repositorio no GitHub."
                    },
                    "repo": {
                        "type": "string",
                        "description": "repositorio no GitHub."
                    },
                    "response_message": {
                        "type": "string",
                        "description": "mensagem."
                    },
                    "issue_number": {
                        "type": "string",
                        "description": "issue numbe"
                    },
                    "github_token": {
                        "type": "string",
                        "description": "Token de autentica\u00e7\u00e3o do GitHub."
                    }
                },
                "required": [
                    "repo",
                    "response_message",
                    "issue_number",
                    "github_token"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_repo_structure",
            "description": "Obtem o a estrutura do repositorio GitHub.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "Nome do repositorio no GitHub."
                    },
                    "repo_owner": {
                        "type": "string",
                        "description": "Nome do dono do repositorio no GitHub."
                    },
                    "github_token": {
                        "type": "string",
                        "description": "Token de autenticacao "
                    },
                    "branch_name": {
                        "type": "string",
                        "description": "Nome da branch principal geralmente main."
                    }
                },
                "required": [
                    "repo_name",
                    "repo_owner",
                    "github_token",
                    "branch_name"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "autogetfilecontent",
            "description": "Obtem o conteudo do arquivo em um repositorio GitHub.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "Nome do repositorio no GitHub."
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Caminho relativo junto ao arquivo"
                    },
                    "branch_name": {
                        "type": "string",
                        "description": "Nome da branch principal geralmente main."
                    },
                    "companyname": {
                        "type": "string",
                        "description": "Nome da organizacao/compania"
                    },
                    "github_token": {
                        "type": "string",
                        "description": "Token de autenticacao "
                    }
                },
                "required": [
                    "repo_name",
                    "file_path",
                    "branch_name",
                    "companyname",
                    "github_token"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "autounittests",
            "description": "\nHere\u2019s a description for the code function arguments:\n\nThe `autounittests` function reads test files and executes the tests contained within. It returns an exit code from `pytest.main([test_file])`, indicating whether all tests passed (exit code 0) or some failed (exit code > 0). The function takes a single parameter, `test_file`, which is the path to the test file.\n\n```python\ndef autounittests(test_file: str) -> int:\n    \"\"\"\n    Execute test files and returns the exit code from pytest.\n\n    Args:\n        test_file: Path to the test file to run.\n\n    Returns:\n        int: Exit code from pytest. 0 if all tests passed, >0 if some failed.\n    \"\"\"\n```",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_file": {
                        "type": "string",
                        "description": "Descri\u00e7\u00e3o do argumento test_file."
                    }
                },
                "required": [
                    "test_file"
                ]
            }
        }
    }
]