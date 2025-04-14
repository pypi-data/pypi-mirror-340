import matplotlib.pyplot as plt

def criar_grafico(tipo, dados, titulo="", xlabel="", ylabel="", salvar_em=None):
    """
    Cria e opcionalmente salva gráficos de linha, barra ou pizza.

    Args:
        tipo (str): Tipo de gráfico ('linha', 'barra', 'pizza').
        dados (dict): Dados para o gráfico.
        titulo (str): Título do gráfico.
        xlabel (str): Rótulo do eixo X (linha/barra).
        ylabel (str): Rótulo do eixo Y (linha/barra).
        legenda (list): Legenda opcional (linha/barra).
        salvar_em (str): Caminho do arquivo para salvar (ex: 'grafico.png'). Se None, exibe o gráfico.
    """
    plt.figure(figsize=(8, 5))

    if tipo == 'linha':
        plt.plot(dados['x'], dados['y'], marker='o')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    elif tipo == 'barra':
        plt.bar(dados['x'], dados['y'])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    elif tipo == 'pizza':
        plt.pie(dados['valores'], labels=dados['labels'], autopct='%1.1f%%', startangle=90)
        plt.axis('equal')

    else:
        raise ValueError("Tipo de gráfico não suportado. Use 'linha', 'barra' ou 'pizza'.")

    plt.title(titulo)

    plt.tight_layout()

    if salvar_em:
        plt.savefig(salvar_em, dpi=300)
        print(f"Gráfico salvo em: {salvar_em}")
        plt.close()
    else:
        plt.show()