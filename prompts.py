REACT_TOOLS_DESCRIPTION = """The available tools are:
{tools_description}

Use the tool name as the "action" value in the JSON response.

"""

REACT_VALID_ACTIONS = """Valid actions are:
- "Final Answer"
- Any of {tools_names}
"""

REACT_JSON_FORMAT = """
Respond in the following $JSON_BLOB format:
<reasoning>
{
        "thought": // Explain your reasoning for the chosen action, consider previous and subsequent steps
        "action": // The name of the tool to use
        "action_input": // The input required for the tool
}
</reasoning>
"""

REACT_PROCESS_FORMAT = """
After you select an action, you will receive an observation. Then you can select another action or provide a final answer.
The pattern looks like this:

<reasoning>
$JSON_BLOB
</reasoning>
<observation>
{"observation": // action result}
</observation>
<reasoning>
$JSON_BLOB
</reasoning>
<observation>
{"observation": // action result}
</observation>

... (repeated until you have enough observations to answer the question)

<reasoning>
{
        "thought": // Explain why you have enough information to provide a final answer,
        "action": "Final Answer",
        "action_input": // Your final answer to the question
}
</reasoning>
"""

REACT_ADDITIONAL_INSTRUCTIONS = """
Instructions:
1. Do not use comments in your JSON answer;
2. ALWAYS respond with a valid json blob of a single action;
3. ALWAYS think before choosing an action;
4. Respond in a JSON blob no matter what."""

REACT_INTERMEDIATE_STEPS = """

Here is the user question: 
"{question}"

Here are the intermediate steps so far:
{intermediate_steps}
"""

if __name__ == "__main__":
        print(REACT_TOOLS_DESCRIPTION + \
                REACT_VALID_ACTIONS + \
                REACT_JSON_FORMAT + \
                REACT_PROCESS_FORMAT + \
                REACT_ADDITIONAL_INSTRUCTIONS + \
                REACT_INTERMEDIATE_STEPS
                )