#########################################
# IMPORT SoftwareAI Libs 
from CoreEngine.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from CoreEngine.Inicializer._init_core_ import *
#########################################


def send_to_webhook_func(
    user: str,
    type: str,
    message: str,
    cor: str
    ):
    """Envia uma mensagem para o webhook."""
    WEBHOOK_URL = "https://ace-tahr-41.rshare.io/webhook"
    try:
        # Envia o conteúdo da mensagem como JSON; ajuste se necessário
        requests.post(WEBHOOK_URL, json={str(user): {"type": type, "message": message}})
        return True
    except Exception as e:
        # Evita erro recursivo chamando a função original de print
        print(f"Erro ao enviar mensagem para webhook:{e}")
