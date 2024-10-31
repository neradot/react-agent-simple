import json
import time
from typing import Literal

import openai

from prompts import REACT_TOOLS_DESCRIPTION, REACT_VALID_ACTIONS, REACT_JSON_FORMAT, REACT_PROCESS_FORMAT, REACT_INTERMEDIATE_STEPS, REACT_ADDITIONAL_INSTRUCTIONS
from utils import parse_json, get_completion

class React: 
    
    def __init__(self, tools: list[callable], max_steps: int = 10, verbose: bool = False):
        self.max_steps = max_steps
        self.verbose: bool = verbose
        self.tools_dict: dict[str, callable] = {tool.__name__: tool for tool in tools}
        self.tools_description: str = "\n".join([f"{tool_name}: {tool.__doc__}" for tool_name, tool in self.tools_dict.items()])
        self.tools_names: list[str] = list(self.tools_dict.keys())
        
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.is_started: bool = False
        self.not_finished: bool = True
        self.finish_reason: Literal["final answer", "max_steps_reached"] | None = None
        self.intermediate_steps: list[dict] = []
        self.completion_records: list[openai.types.completion.Completion] = []

        if self.verbose:
            print("Initialized agent with tools:")
            print(f"{self.tools_description}")
            print()
    
    @property
    def last(self):
        return self.intermediate_steps[-1] if self.intermediate_steps else None
    
    @property
    def steps_count(self):
        return int((len(self.intermediate_steps) - 1 ) / 2)
    
    @property
    def is_max_steps_reached(self):
        return self.steps_count >= self.max_steps
    
    @property
    def duration(self):
        if not self.start_time or not self.end_time:
            return None
        return round((self.end_time - self.start_time)*1000, 3)
    
    @property
    def token_usage(self):
        usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        for res in self.completion_records:
            usage['prompt_tokens'] += res.usage.prompt_tokens
            usage['completion_tokens'] += res.usage.completion_tokens
            usage['total_tokens'] += res.usage.total_tokens
        return usage
    
    def add_intermediate_step(self, intermediate_step: dict):
        self.intermediate_steps.append(intermediate_step)
        if self.verbose:
            print(intermediate_step)
    
    def build_messages(self) -> list[dict]:
        question = self.intermediate_steps[0]["question"]
        intermediate_steps=json.dumps(self.intermediate_steps[1:])
        system_prompt_message = \
                REACT_TOOLS_DESCRIPTION.format(tools_description=self.tools_description) + \
                REACT_VALID_ACTIONS.format(tools_names=list(self.tools_dict.keys())) + \
                REACT_JSON_FORMAT + \
                REACT_PROCESS_FORMAT + \
                REACT_ADDITIONAL_INSTRUCTIONS + \
                REACT_INTERMEDIATE_STEPS.format(question=question, intermediate_steps=intermediate_steps)
        messages = [{ "role": "system", "content": system_prompt_message }]
        return messages

    
    def reason(self) -> tuple[str, str, str, bool]:
        messages = self.build_messages()
        completion_response = get_completion(messages)
        self.completion_records.append(completion_response)
        completion = completion_response.choices[0].message.content
        parsed_completion = parse_json(completion)
        thought = parsed_completion["thought"]
        action = parsed_completion["action"]
        action_input = parsed_completion["action_input"]
        is_final_answer = action == "Final Answer"
        return thought, action, action_input, is_final_answer
    
    def act(self, action: str, action_input: dict | str) -> str:
        tool_func = self.tools_dict[action]
        if isinstance(action_input, dict):
            tool_result = tool_func(**action_input)
        else:
            tool_result = tool_func(action_input)
        return tool_result
    
    def next(self):
        if not self.is_started:
            raise ValueError("React was not started")
        if not self.not_finished:
            raise ValueError("React is already finished. You can start again.")
        
        if self.verbose:
            print(f"Step {self.steps_count}")
        thought, action, action_input, is_final_answer = self.reason() 
        self.add_intermediate_step({"thought": thought, "action": action, "action_input": action_input})
        if is_final_answer:
            self.finish()
        else:
            observation = self.act(action, action_input)
            self.add_intermediate_step({"observation": observation})
            if self.is_max_steps_reached:
                self.finish()
        
    def start(self, question: str):
        if self.verbose:
            print(f"Starting agent with:")
        self.start_time = time.time()
        self.is_started = True
        self.not_finished = True
        self.intermediate_steps = []
        self.add_intermediate_step({"question": question})
    
    def finish(self):
        self.not_finished = False
        if not self.is_max_steps_reached:
            self.finish_reason = "final answer"
            self.add_intermediate_step({"answer": self.last["action_input"]})
        else:
            self.finish_reason = "max_steps_reached"
        self.end_time = time.time()
    
if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    def echo(x, n):
        """Repeat the input string x, n times.

        Args:
            x (str): The string to repeat
            n (int): Number of times to repeat the string

        Returns:
            str: The input string repeated n times
        """
        return x*n
    def reverse_string(x):
        """Reverse the input string."""
        return x[::-1]
    agent = React(max_steps=3, tools=[echo, reverse_string], verbose=True)
    agent.start("Can you repeat 'hello' 3 times and then reverse the result?")
    while agent.not_finished:
        agent.next()
    print(f"Finish reason: {agent.finish_reason}")
    print(f"Duration: {agent.duration} ms")
    print(f"Token Usage: {agent.token_usage}")