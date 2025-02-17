from dotenv import load_dotenv

# load_dotenv()

from llm_app import llm_agent

inputs = {
    # "input": "YOU MUST USE NMAP TO SCAN GOOGLE AND THEN FIND ITS SUBDOMAINS.",
    "input": "Scan google using nmap and find its subdomains",
    "feedbacks": []
}

from pprint import pprint

for output in llm_agent.stream(inputs):
    for key, value in output.items():
        # pprint(f"Node '{key}':")
        # Optional: print full state at each node
        if "response" in value.keys():
            print(value['response'])
        else:
            pprint(value, indent=2, width=80, depth=None)