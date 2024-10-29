REACT_GUIDELINES = """
You have access to the following tools:

{tools_description}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tools_names} or "None"

Provide only ONE action per $JSON_BLOB, as shown:

```json
{{
        "thought": // consider previous and subsequent steps and decide what action to take,
        "action": $TOOL_NAME (or "Final Answer" or "None" if no action is taken),
        "action_input": $INPUT
}}
```

Follow this format:
Question: input question to answer
```
$JSON_BLOB
```
Observation: action result
```
$JSON_BLOB
```
Observation: action result
... (repeat this pattern until you have enough observations to answer the question)
```json
{{
        "thought": // Explain why do you think you have enough information to answer the question,
        "action": "Final Answer",
        "action_input": // Final response to human
}}
```
"""

INTERMEDIATE_STEPS = """Question: "{question}"

{intermediate_steps}

(reminder to respond in a JSON blob no matter what)"""

ADDITIONAL_INSTRUCTIONS="""Instructions:
1. Do not use comments in your JSON answer.
2. ALWAYS respond with a valid json blob of a single action. 
3. ALWAYS think before choosing an action."""