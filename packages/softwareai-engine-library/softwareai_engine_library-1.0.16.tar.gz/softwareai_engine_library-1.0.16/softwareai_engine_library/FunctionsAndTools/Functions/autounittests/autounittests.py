import sys
import pytest

def autounittests(test_file: str) -> int:
    """
    Executa os testes do arquivo fornecido e retorna o código de saída do pytest.
    Código 0 indica que todos os testes passaram.
    """
    exit_code = pytest.main([test_file])
    if exit_code == 0:
        print("Todos os testes passaram.")
    else:
        print("Alguns testes falharam.")
    return exit_code
