import subprocess
from gemini_helper import get_kubectl_command

namespacename = None

def run_kubectl_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error: {str(e)}"
    
def logs(user_input):

    global namespacename
    parts = user_input.split("pod")
    pod_name = parts[-1].strip()

    if  "follow" in user_input and "logs" in user_input:
        if namespacename is None:
            print("Bot: Please specify the namespace first. Use 'use namespace <namespace>' to set it.")
        else:
            output = run_kubectl_command(f"kubectl logs -f {pod_name} -n {namespacename}")
            print("Bot:\n" + output)

    elif "logs" in user_input:
        if namespacename is None:
            print("Bot: Please specify the namespace first. Use 'use namespace <namespace>' to set it.")
        else:
            output = run_kubectl_command(f"kubectl logs {pod_name} -n {namespacename}")
            print("Bot:\n" + output)        

def main():
    global namespacename    
    print("👋 Welcome to KubeBot! Type 'exit', 'quit' or 'bye' to quit.")

    while True:
        user_input = input("You: ").lower()

        if user_input in ["exit", "quit", "bye"]:
                print("Bot: Goodbye, Harshal!")
                break
        
        elif "use" in user_input and "namespace" in user_input:
            parts = user_input.split("namespace")
            namespace = parts[-1].strip()
            namespacename = namespace
            print(f"Bot: Namespace set to '{namespacename}'. You can now run commands in this namespace.")

        elif "show" in user_input and "namespaces" in user_input:
            output = run_kubectl_command("kubectl get deployments --all-namespaces=true")
            print("Bot:\n" + output)

        elif "show" in user_input and "pods" in user_input:
            if namespacename is None:
                print("Bot: Please specify a namespace first using 'use namespace <namespace>'.")
            elif "in" in user_input:
                parts = user_input.split("in")
                namespace = parts[-1].strip()
                namespacename = namespace
                print(f"Bot: Namespace set to '{namespacename}'. You can now run commands in this namespace.")
                output = run_kubectl_command(f"kubectl get pods -n {namespace}")
                print("Bot:\n" + output)      
            elif namespacename is not None:
                output = run_kubectl_command(f"kubectl get pods -n {namespacename}")
                print("Bot:\n" + output) 
            else:
                print("Bot: Something went wrong.")

        elif "logs" in user_input:
            logs(user_input)
        
        else:
            print("Bot: Sorry, I don't understand that yet.")

        

if __name__ == "__main__":
    main()