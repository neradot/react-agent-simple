REACT_TOOLS_DESCRIPTION = """The available tools are:
{tools_description}

Use the tool name as the "action" value in the JSON response.
"""

REACT_VALID_ACTIONS = """Valid actions are:
- "Final Answer"
- Any of {tools_names}"""

REACT_JSON_FORMAT = """
Respond in the following $JSON_BLOB format:
```json
{{
        "thought": // Explain your reasoning for the chosen action, consider previous and subsequent steps
        "action": // The name of the tool to use
        "action_input": // The input required for the tool
}}
```
"""

REACT_PROCESS_FORMAT = """
After you select an action, you will receive an observation. Then you can select another action or provide a final answer.
The pattern looks like this:
```
$JSON_BLOB
```
{{"observation": // action result}}
```
$JSON_BLOB
```
{{"observation": // action result}}
... (repeated until you have enough observations to answer the question)
```json
{{
        "thought": // Explain why you have enough information to provide a final answer,
        "action": "Final Answer",
        "action_input": // Your final answer to the question
}}
```
"""

REACT_ADDITIONAL_INSTRUCTIONS = """Instructions:
1. Do not use comments in your JSON answer;
2. ALWAYS respond with a valid json blob of a single action;
3. ALWAYS think before choosing an action;
4. Respond in a JSON blob no matter what."""

REACT_INTERMEDIATE_STEPS = """Question: "{question}"

{intermediate_steps}
"""

