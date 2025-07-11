import subprocess
import re
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
    if "pod" not in user_input:
        return "Bot: Please specify the pod name after 'logs pod <name>'."

    pod_name = user_input.split("pod")[-1].strip()

    if not namespacename:
        return "Bot: Please set a namespace first using 'use namespace <name>'."

    if "follow" in user_input:
        return run_kubectl_command(f"kubectl logs -f {pod_name} -n {namespacename}")
    else:
        return run_kubectl_command(f"kubectl logs {pod_name} -n {namespacename}")

def clean_gemini_output(raw_cmd):
    # Removes markdown formatting and backticks
    cleaned = re.sub(r"```(bash|shell)?", "", raw_cmd)
    cleaned = cleaned.replace("```", "").strip()
    return cleaned

def main():
    global namespacename    
    print("👋 Welcome to KubeBot! Type 'exit', 'quit' or 'bye' to quit.")

    while True:
        user_input = input("You: ").lower().strip()

        if user_input in ["exit", "quit", "bye"]:
            print("Bot: Goodbye, Harshal!")
            break

        elif "use namespace" in user_input:
            parts = user_input.split("namespace")
            namespace = parts[-1].strip()
            namespacename = namespace
            print(f"Bot: Namespace set to '{namespacename}'.")

        elif "show namespaces" in user_input:
            output = run_kubectl_command("kubectl get namespaces")
            print("Bot:\n" + output)

        elif "show pods" in user_input:
            if "in" in user_input:
                parts = user_input.split("in")
                namespace = parts[-1].strip()
                namespacename = namespace
                output = run_kubectl_command(f"kubectl get pods -n {namespace}")
                print("Bot:\n" + output)      
            elif namespacename:
                output = run_kubectl_command(f"kubectl get pods -n {namespacename}")
                print("Bot:\n" + output)
            else:
                print("Bot: Please specify a namespace first using 'use namespace <namespace>'.")

        elif "logs" in user_input:
            output = logs(user_input)
            print("Bot:\n" + output)

        else:
            # Gemini fallback
            print("Bot: Let me try to figure this out using Gemini 🤖...")
            raw_cmd = get_kubectl_command(user_input)

            if raw_cmd.lower().startswith("error"):
                print("Bot: Failed to get a command from Gemini.")
                continue

            kubectl_cmd = clean_gemini_output(raw_cmd)

            # Inject namespace if relevant and missing
            if namespacename and "-n" not in kubectl_cmd:
                kubectl_cmd += f" -n {namespacename}"

            print(f"Bot (Gemini): Running → {kubectl_cmd}")
            output = run_kubectl_command(kubectl_cmd)
            print("Bot:\n" + output)

if __name__ == "__main__":
    main()
