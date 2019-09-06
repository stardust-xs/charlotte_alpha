"""
The connect module: Enables access to Charlotte using an external connector.

These classes help you talk to Charlotte using other methods than command line.
As of now, only Google Assistant is supported for testing.

At a glance, the structure if the module is following:
 - Assistant():         A custom HTTP input channel using Google Assistant.
                        This implementation is the basis for a custom
                        implementation of a chat frontend. You can customize
                        this to send messages to Rasa Core and retrieve
                        responses from the agent.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.0 - First code.

from sanic import Blueprint
from sanic.response import json

from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import CollectingOutputChannel

from charlotte.utils.assists.profile import lower


class Assistant(InputChannel):
    """A custom http input channel."""

    @classmethod
    def name(cls):
        # Name of the class.
        return 'assistant'

    def blueprint(self, on_new_message):
        assistant_webhook = Blueprint('assistant_webhook', __name__)

        # Checking health of the connection.
        @assistant_webhook.route('/', methods=['GET'])
        async def health(request):
            return json({"status": "working"})

        # Sending response back.
        @assistant_webhook.route('/charlotte', methods=['POST'])
        async def receive(request):
            payload = request.json
            intent = payload['inputs'][0]['intent']
            text = payload['inputs'][0]['rawInputs'][0]['query']
            # If the session is just started, greet user else reply back
            # using the response from Rasa.
            if intent == 'actions.intent.MAIN':
                message = 'Hello, I\'m Charlotte. Your personal assistant!'
            else:
                out = CollectingOutputChannel()
                await on_new_message(UserMessage(text, out))
                responses = [reply['text'] for reply in out.messages]
                message = responses[0]
            # Google Assistant Actions JSON template.
            response = {
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
                                            "showText": message
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
            return json(response)
        return assistant_webhook
