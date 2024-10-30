import json
import time

import openai
from prompts import REACT_TOOLS_DESCRIPTION, REACT_VALID_ACTIONS, REACT_JSON_FORMAT, REACT_PROCESS_FORMAT, REACT_INTERMEDIATE_STEPS, REACT_ADDITIONAL_INSTRUCTIONS
from utils import parse_json
class React:
    def __init__(self, tools: list[callable], max_steps: int = 10, verbose: bool = False):
        self.openai_client = openai.OpenAI()
        self.intermediate_steps = []
        self.completion_responses = []
        self.is_started = False
        self.not_finished = True
        self.finish_reason = None
        self.max_steps = max_steps
        self.start_time = None
        self.end_time = None
        self.tools_dict = {tool.__name__: tool for tool in tools}
        self.verbose = verbose
        print("React initialized with tools:")
        print(self.tools_description)
    
    @property
    def last(self):
        return self.intermediate_steps[-1] if self.intermediate_steps else None
    
    @property
    def steps_count(self):
        return (len(self.intermediate_steps) - 1 ) / 2
    
    @property
    def is_max_steps_reached(self):
        return self.steps_count >= self.max_steps
    
    @property
    def tools_description(self):
        return "\n".join([f"{tool_name}: {tool.__doc__}" for tool_name, tool in self.tools_dict.items()])
    
    @property
    def tools_names(self):
        return [tool.__name__ for tool in self.tools]
    
    @property
    def duration(self):
        if not self.start_time or not self.end_time:
            return None
        return round((self.end_time - self.start_time)*1000, 3)
    
    @property
    def token_usage(self):
        usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        for res in self.completion_responses:
            usage['prompt_tokens'] += res.usage.prompt_tokens
            usage['completion_tokens'] += res.usage.completion_tokens
            usage['total_tokens'] += res.usage.total_tokens
        return usage
    
    def add_step(self, step: dict):
        self.intermediate_steps += [step]
        if self.verbose:
            print(step)
    
    def build_messages(self):
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
    
    def completion(self, messages):
        model = "gpt-4o"
        response = self.openai_client.chat.completions.create(messages=messages, model=model)
        self.completion_responses += [response]
        return response.choices[0].message.content
    
    def reason(self):
        messages = self.build_messages()
        completion = self.completion(messages)
        parsed_completion = parse_json(completion)
        thought = parsed_completion["thought"]
        action = parsed_completion["action"]
        action_input = parsed_completion["action_input"]
        is_final_answer = action == "Final Answer"
        return thought, action, action_input, is_final_answer
    
    def act(self, action, action_input):
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
        
        thought, action, action_input, is_final_answer = self.reason() 
        self.add_step({"thought": thought, "action": action, "action_input": action_input})
        if is_final_answer:
            self.finish()
        else:
            observation = self.act(action, action_input)
            self.add_step({"observation": observation})
            if self.is_max_steps_reached:
                self.finish()
        
    def start(self, question: str):
        self.start_time = time.time()
        self.is_started = True
        self.not_finished = True
        self.intermediate_steps = []
        self.add_step({"question": question})
        self.next()
    
    def finish(self):
        self.not_finished = False
        if not self.is_max_steps_reached:
            self.finish_reason = "final answer"
            self.add_step({"answer": self.last["action_input"]})
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