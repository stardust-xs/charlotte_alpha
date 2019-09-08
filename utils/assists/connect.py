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
#   1.0.2 - Added reference link to the code.
#   1.0.0 - First code.

import logging
import json
from sanic import Blueprint, response
from sanic.request import Request

from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import CollectingOutputChannel

from charlotte.utils.assists.profile import lower


class Assistant(InputChannel):
    """A custom http input channel."""
    # You can find the reference code here:
    # https://medium.com/rasa-blog/going-beyond-hey-google-building-a-rasa-powered-google-assistant-5ff916409a25
    @classmethod
    def name(cls):
        # Name of the class.
        return 'assistant'

    def blueprint(self, on_new_message):

        google_webhook = Blueprint('google_webhook', __name__)

        @google_webhook.route("/", methods=['GET'])
        async def health(request):
            return response.json({"status": "ok"})

        @google_webhook.route("/webhook", methods=['POST'])
        async def receive(request):
            payload = request.json
            intent = payload['inputs'][0]['intent']
            text = payload['inputs'][0]['rawInputs'][0]['query']

            if intent == 'actions.intent.MAIN':
                message = "Hello! Welcome to the Rasa-powered Google Assistant skill. You can start by saying hi."
            else:
                out = CollectingOutputChannel()
                await on_new_message(UserMessage(text, out))
                responses = [m["text"] for m in out.messages]
                message = responses[0]
            r = {
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

            return response.json(r)

        return google_webhook
