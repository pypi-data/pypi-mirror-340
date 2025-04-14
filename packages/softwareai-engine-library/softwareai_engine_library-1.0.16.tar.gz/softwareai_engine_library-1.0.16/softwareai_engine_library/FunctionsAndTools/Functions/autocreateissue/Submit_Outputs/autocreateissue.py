

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
def submit_output_autocreateissue(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):
    global tool_outputs



    if function_name == 'autocreateissue':
        args = json.loads(function_arguments)
        result = autocreateissue(
            repo_owner=args['repo_owner'],
            repo_name=args['repo_name'],
            issue_title=args['issue_title'],
            issue_body=args['issue_body'],
            githubtoken=args['githubtoken']
        )

        tool_outputs.append({
        "tool_call_id": tool_call.id,
        "output": json.dumps(result)
        })

    # Submit all tool outputs at once after collecting them in a list
    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=threead_id,
            run_id=run.id,
            tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
            tool_outputs = []
            return True
        except Exception as e:
            print("Failed to submit tool outputs:", e)
            try:
                client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=threead_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
                tool_outputs = []
                return True
            except:
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=threead_id,
                    run_id=run,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
                tool_outputs = []
                return True
    else:
        print("No tool outputs to submit.")
