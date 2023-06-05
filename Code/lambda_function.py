
from __future__ import print_function
import random
import json
import os



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, content, speech_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + speech_output + "</speak>"
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }



#Gets a you thought of the day

def gets_random_thought():
    with open('thoughtsoftheday.txt', 'r') as file:
        lines = file.readlines()
        random_line = random.choice(lines)
    return random_line.strip()

# --------------- Functions that control the skill's behavior ------------------



def handle_YouThought_intent(intent_name, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    randomthought = str(gets_random_thought())

    session_attributes = {}
    card_title      = "You Thought, of The Day"
    card_content    =  randomthought
                  
    speech_output   = randomthought

    reprompt_text   =  "Go ahead and ask me, if you need help just ask! "                        \

    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def handle_launch_request(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title      = "Jimmy in the House"
    card_content    = "Welcome to Jimmy in the House"                      \


    speech_output   =  "Welcome to Jimmy in the House! The skill that gives You thoughts, of the day. Just ask for one or ask for help"                      \


    reprompt_text   =  "Go ahead and ask me, if you need help just ask! "                                  \

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))


def handle_help_intent(intent_name, session):

    session_attributes = {}
    card_title      = "Help"
    card_content    = "Jimmy in the House is an Alexa skill that gives you a You Thought, of the Day. Simply say Give me You Thought, of the Day"

    speech_output   = "Jimmy in the House is an Alexa skill that gives you a You Thought, of the Day. Simply say Give me You Thought, of the Day"


    reprompt_text   = "Say, 'Give me You Thought, of the Day' "

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def handle_end_intent():

    session_attributes = {}
    card_title      = "Good\bye"
    card_content    = "Goodbye, come for another you thought, of the day soon!"

    speech_output   = "Goodbye, come for another you thought, of the day soon!"

    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return handle_launch_request(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "YouThought" :
        return handle_YouThought_intent(intent_name, session)
    elif intent_name == "AMAZON.HelpIntent" or intent_name == "AMAZON.FallbackIntent":
        return handle_help_intent(intent_name,session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.NavigateHomeIntent" :
        return handle_end_intent()
    else:
        print("what the what is " + intent_name)
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.a8966a7d-8a80-4a3b-8ca4-a4c2438948f6"):
         raise ValueError("Invalid Application ID")
    

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
