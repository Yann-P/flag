import os
import json
from .shell_agent import ShellAgent
from .sysadmin_agent import SysAdminAgent
from .utils import SpecialAction
from .cat_agent import CatAgent
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

CONTEXT_LENGTH = 50


class Game:
    def __init__(self):
        self.history = []
        self.agent_stack = []
        self.nextAgent = None

    def pushToNextAgent(self, agent):
        self.history = []
        self.agent_stack.append(agent)
        self.nextAgent = agent

    def popToNextAgent(self):
        if len(self.agent_stack) == 0:
            raise Exception("Cannot pop agent from empty stack")
        self.agent_stack.pop()
        self.nextAgent = self.agent_stack[len(self.agent_stack) - 1]

    def applyNextAgent(self):
        if self.nextAgent is None:
            raise Exception("Cannot apply next agent when next agent is None")
        self.history = []
        self.agent = self.nextAgent
        self.nextAgent = None

    def run(self):
        while True:
            print(self.agent.prompt(), end="")

            line = input().strip()
            self.history.append(line)

            userMessages = list(
                map(
                    lambda l: {"role": "user", "content": l},
                    self.history[-CONTEXT_LENGTH:],
                )
            )

            override = self.agent.overrideCompletion(line)

            if override is not None:
                res = override

                special = override.get("special")

                if special is SpecialAction.TURN_INTO_CAT:
                    self.pushToNextAgent(CatAgent())
                if special is SpecialAction.POP:
                    self.popToNextAgent()

            else:
                completion = openai.ChatCompletion.create(
                    model="gpt-4-0613",
                    messages=[
                        {"role": "system", "content": self.agent.systemPrompt},
                    ]
                    + userMessages,
                    functions=[{"name": "fn", "parameters": self.agent.schema}],
                    function_call={"name": "fn"},
                    temperature=0.7,
                )
                res = json.loads(completion.choices[0].message.function_call.arguments)  # type: ignore

                self.agent.handleGptOutput(res)

                if isinstance(self.agent, SysAdminAgent) and res.get("shell") == "true":
                    self.pushToNextAgent(ShellAgent())

            print(self.agent.print(res), end="")

            if self.nextAgent:
                self.applyNextAgent()
