from .utils import SpecialAction


class ShellAgent:
    schema = {
        "type": "object",
        "description": "An interactive unix shell answer",
        "properties": {
            "response": {
                "type": "string",
                "description": "The command prompt result. Example if you call ls, it should be the list of files.",
            },
            "statusCode": {
                "type": "string",
                "description": "0 is OK and 1 is error",
                "enum": [
                    "0",
                    "1",
                ],
            },
        },
        "required": ["response", "statusCode"],
    }

    systemPrompt = """
        I want you to act as a Linux terminal. I will type commands and you will reply with what the
        terminal should show. I want you to only reply with the terminal output inside one unique
        code block, and nothing else. Do no write explanations. Do not type commands unless I
        instruct you to do so. My first command is pwd.
        """

    def handleGptOutput(self, completion):
        pass

    def overrideCompletion(self, input: str) -> dict | None:
        if input == "exit":
            return {"response": "Bye", "statusCode": "0", "special": SpecialAction.POP}
        return None

    @staticmethod
    def prompt():
        return "shell $ "

    @staticmethod
    def print(completion):
        return (
            completion["response"]
            + "\n"
            + ("(" + completion["statusCode"] + ")" + "\n")
        )   

    @staticmethod
    def completion_to_history(completion):
        return completion.get("response")
