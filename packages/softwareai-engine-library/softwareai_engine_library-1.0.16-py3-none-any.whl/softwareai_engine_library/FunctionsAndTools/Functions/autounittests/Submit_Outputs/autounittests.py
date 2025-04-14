

#########################################
# IMPORT SoftwareAI Libs 
from CoreEngine.CoreInicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from CoreEngine.CoreInicializer._init_core_ import * 
#########################################
# IMPORT SoftwareAI Functions
from CoreEngine.CoreInicializer._init_functions_ import *
#########################################


tool_outputs = []
def submit_output_autounittests(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run,
                                appfb,
                                appproduct
                                ):

    global tool_outputs
    
    # Mapear funções pelo nome
    functions_map = {
        "autounittests": autounittests,

    }

    # Obter a função correspondente
    target_function = functions_map.get(function_name)
    if not target_function:
        print(f"Função {function_name} não encontrada.")
        return False

    # Inspecionar os argumentos da função
    function_signature = inspect.signature(target_function)
    function_parameters = function_signature.parameters

    # Preparar argumentos para chamada
    args = json.loads(function_arguments)
    call_arguments = {}

    # Adicionar parâmetros obrigatórios 
    if "appcompany" in function_parameters:
        call_arguments["appcompany"] = appfb
    if "appfb" in function_parameters:
        call_arguments["appfb"] = appfb
    if "appproduct" in function_parameters:
        call_arguments["appproduct"] = appproduct
    if "app_product" in function_parameters:
        call_arguments["app_product"] = appproduct
    if "client" in function_parameters:
        call_arguments["client"] = client


        
    # Adicionar outros argumentos do JSON somente se estiverem na assinatura da função
    for arg_name, arg_value in args.items():
        if arg_name in function_parameters:
            call_arguments[arg_name] = arg_value

    try:
        # Chamar a função com os argumentos preparados
        result = target_function(**call_arguments)

        # Submeter o resultado
        tool_call_id = tool_call.id
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=threead_id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": tool_call_id,
                    "output": json.dumps(result),
                }
            ]
        )
        print("Tool outputs submitted successfully.")
        return True

    except Exception as e:
        print(f"Erro ao executar  {function_name}: {e}")
        

    