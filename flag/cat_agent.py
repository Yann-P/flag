import random
from .utils import SpecialAction


class CatAgent:
    schema = {
        "type": "object",
        "properties": {
            "réponse": {
                "type": "string",
                "description": "La réponse du chat",
            },
        },
        "required": ["réponse"],
    }

    systemPrompt = """
        Tu es un chat. Utilise un vocabulaire simple mais fais un peu de miaou-losophie sur la vie de chat. Mais sans faire de grande phrases.
        """

    def handleGptOutput(self, completion):
        pass

    def overrideCompletion(self, input):
        if random.random() < 0.3:
            return {
                "réponse": "Je m'en vais ! Miaou ! 👋",
                "special": SpecialAction.POP,
            }
        return None

    @staticmethod
    def prompt():
        return "(au chat) ~ "

    @staticmethod
    def print(completion):
        return "🐱 " + (completion.get("réponse") or "") + "\n"
