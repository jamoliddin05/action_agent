import os

from langgraph.graph import END, StateGraph, START

from graph_components.nodes import should_answer, validate_syntax, generate_command, should_pass_validation, execute
from graph_components.states.graph_state import GraphState


workflow = StateGraph(GraphState)
workflow.add_node("command_generator", generate_command)
workflow.add_node("validate_syntax", validate_syntax)
workflow.add_node("execute", execute)

workflow.add_conditional_edges(
    START,
    should_answer,
    {
        "command_generator": "command_generator",
        "not_relevant": END
    }
)

workflow.add_edge("command_generator", "validate_syntax")

workflow.add_conditional_edges(
    "validate_syntax",
    should_pass_validation,
    {
        "command_generator": "command_generator",
        "execute": "execute"
    }
)

workflow.add_edge("execute", END)

app = workflow.compile()

# from IPython.display import display, Image
#
# png_graph = app.get_graph().draw_mermaid_png()
# with open("my_graph.png", "wb") as f:
#     f.write(png_graph)
#
# print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

from pprint import pprint

# # Run
# state = GraphState(input="What player at the Bears expected to draft first in the 2024 NFL draft?")
#
# for output in app.stream(state):
#     print(output['input'])

inputs = {
    "input": "Scan google using nmap",
    "feedbacks": []
}
for output in app.stream(inputs):
    print(output)