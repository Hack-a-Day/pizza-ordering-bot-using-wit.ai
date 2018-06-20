# pizzawit - Talks to wit.ai for speech recognition and analysis in order
# to make a pizza-ordering chatbot. No actual phone call is made.
#
# See here for details: https://hackaday.com/?p=312908
#
# Copyright (c) 2018 - Steven Dufresne
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject 
# to the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
from wit import Wit

# Put your access token from wit here. Get this from your App's Settings on
# https://wit.ai. The Server Access Token works.
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' 

client = Wit(access_token)

def do_wit_natural_language_processing(audio_file):
    # do_wit_natural_language_processing - Have Wit.ai process the given
    # .wav file to convert the speech to text as well as analyse it and
    # map it to entities which we've trained Wit.ai for and extract any
    # data where appropriate.
    with open(audio_file, 'rb') as f:
        resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
        return resp
    return None

# these are all the things the pizza place will say in the order it will
# say it. If we have an actual phone then this would be replaced by the
# input from the phone
conv_place = 0
conv_numb = 7
conv = ['audio_johnnys_greeting.wav',
        'audio_johnnys_asking_for_toppings.wav',
        'audio_johnnys_asking_is_that_all.wav',
        'audio_johnnys_asking_is_that_all.wav',
        'audio_johnnys_pickup_or_delivery.wav',
        'audio_johnnys_giving_duration.wav',
        'audio_johnnys_bye.wav']

def get_phone_response():
    # get_phone_response - Get the next thing said by the person at the pizza
    # store on the other end of the phone. We pretend and instead just return 
    # the name of the next wave file in our pretend conversation.
    #
    global conv_place
    if conv_place == conv_numb:
        return None
    conv_place += 1
    return conv[conv_place-1]

def first_entity_intent_value(entities, entity):
    # first_entity_intent_value - Given a response from Wit.ai, if it contains
    # an intent with a value, and the value is the same at entity then return
    # the value as confirmation. Everything else returns None.
    #
    if 'intent' not in entities:
        return None
    val = entities['intent'][0]['value']
    if not val:
        return None
    if val != entity:
        return None
    return val['value'] if isinstance(val, dict) else val

coke_ordered = False
while True:

    # get the next thing said by the pizza place, have Wit.ai do natural
    # language processing on it, and also play it to the speaker

    audio_file = get_phone_response()
    if audio_file == None:
        break; # the conversation is finished
    print("%s" % audio_file)
    resp = do_wit_natural_language_processing(audio_file)
    print(resp)
    os.system('aplay ' + audio_file)

    # check if what was said matches any of the things we expected the pizza
    # place to have said

    greeting = first_entity_intent_value(resp['entities'], 'greeting')
    asking_for_toppings = first_entity_intent_value(resp['entities'], 'asking_for_toppings')
    asking_is_that_all = first_entity_intent_value(resp['entities'], 'asking_is_that_all')
    asking_pickup_or_delivery = first_entity_intent_value(resp['entities'], 'asking_pickup_or_delivery')
    give_order_ready_time = first_entity_intent_value(resp['entities'], 'give_order_ready_time')
    bye = first_entity_intent_value(resp['entities'], 'bye')

    # based on what the pizza place said, play an appropriate response to
    # the speaker

    if greeting:
        os.system('aplay audio_customer_greeting_order_pizza.wav')
    elif asking_for_toppings:
        os.system('aplay audio_customer_toppings.wav')
    elif asking_is_that_all:
        if not coke_ordered:
            os.system('aplay audio_customer_one_coke.wav')
            coke_ordered = True
        else:
            os.system('aplay audio_customer_yes.wav')
    elif asking_pickup_or_delivery:
        os.system('aplay audio_customer_for_pickup.wav')
    elif give_order_ready_time:
        pickup_in = resp['entities']['giving_duration'][0]['value']
        print('Pick up in %d minutes' % pickup_in)
        os.system('aplay audio_customer_okay_thanks.wav')
    elif bye:
        os.system('aplay audio_customer_bye.wav')
    else:
        os.system('aplay audio_customer_didnt_understand.wav')
        print('HELP!!!!!!!!')
        break
