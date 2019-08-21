"""
This module enables Charlotte to run via an external connector.

    Note : As of now only Google Assistant is supported.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sanic import Blueprint
from sanic.response import json

from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import CollectingOutputChannel

from charlotte.utils.profiles.default import lower


class Assistant(InputChannel):
    """
    Definition
    ----------
        A custom http input channel.
        This implementation is the basis for a custom implementation of a chat
        frontend. You can customize this to send messages to Rasa Core and
        retrieve responses from the agent.
    """
    @classmethod
    def name(cls):
        return 'assistant'

    def blueprint(self, on_new_message):
        assistant_webhook = Blueprint('assistant_webhook', __name__)

        @assistant_webhook.route('/', methods=['GET'])
        async def health(request):
            return json({"status": "working"})

        @assistant_webhook.route('/charlotte', methods=['POST'])
        async def receive(request):
            payload = request.json
            intent = payload['inputs'][0]['intent']
            text = payload['inputs'][0]['rawInputs'][0]['query']

            if intent == 'actions.intent.MAIN':
                message = 'Hello, I\'m Charlotte. Your personal assistant!'
            else:
                out = CollectingOutputChannel()
                await on_new_message(UserMessage(text, out))
                responses = [reply['text'] for reply in out.messages]
                message = responses[0]
            ai_response = {
                "expectUserResponse": 'true',
                "expectedInputs": [
                    {
                        "possibleIntents": [
                            {
                                "intent": "actions.intent.TEXT"
                            }
                        ],
                        "inputPrompt": {
                            "richInitialPrompt": {
                                "items": [
                                    {
                                        "simpleResponse": {
                                            "textToSpeech": message,
                                            "displayText": message
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]
            }

            return json(ai_response)

        return assistant_webhook
