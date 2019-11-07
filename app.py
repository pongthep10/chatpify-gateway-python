from flask import Flask, request
import requests
import logging
from flask import Flask, jsonify
from logging.handlers import RotatingFileHandler
import json
import flask
line_token ='5tVkug1IAV5LU2RMUNjTziFzset2sLAUEhSC9gIZosB'

url = 'https://notify-api.line.me/api/notify'

def _lineNotify(payload,token,file=None):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)

def lineNotify(message, token):
    try:
        payload = {'message':message}
        resp = _lineNotify(payload,token)
        if resp.status_code==200:
            return resp
        else:
            print('lineNotify: response code:', resp.status_code, resp.text)
    except Exception as e:
        print('lineNotify: ',e.message, e.args)

def notifyFile(filename,msg,token):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message': msg}
    return _lineNotify(payload,token,file)

def notifyPicture(url,token):
    payload = {'message':"",'imageThumbnail':url,'imageFullsize':url}
    return _lineNotify(payload,token)

def notifySticker(msg, stickerID,stickerPackageID,token):
    payload = {'message':msg,'stickerPackageId':stickerPackageID,'stickerId':stickerID}
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=None)
    
    
    
app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'tktk'# <paste your verify token here>


page_token = {      
                '468834046647369':'EAAKDDnoBSygBAI7RbVqTDoMPAl2F0cXvxzEFuUFxZCIdel5RGmEANN4sisCOkp0DFaa5MSZAZBYCLs0y39x9BKZCqZCYPdnNUzWtiiWnGZCcLh7YQVbYsaMECEMbWcp2xvOMNIKB5KzIqmGhnLw5euU4VfmL1tOpXqoREELv4UBgZDZD',#Xtive,
                '105637970864675': 'EAAgZCpzUtPzEBACMtZCJsjqBlfe2ne0u7G9ofnstbuIc719JiuRt2VYdhhYhJPkKSivXyL6BH2jzVOpDC7epbuHNjPLXL0PbDCh0LyVfuIkqFGPiIMPmZC2dyL2UCAaDiNe3X8iuoZAnfMifE96XoF3iSj6Ntvo9uca8WHq0BrY50nxahrqj',#testy
                '333353574031688':'EAAKDDnoBSygBAAN02M1gZB9ikgWxnRtZB67EjAyYpQ9qOpAIutHMZBaZBRHEGwWyvlLo5ksdC9EBZBROENQZCeNvLZBYYnICjcUaXatFf9aynZBbLWi6ZCcItzegN2skv4P26FIUUJSJGDtp5EOkcSSmJPGmv8RuWZCrZByZCjpzZBDNxKwZDZD' #HH
                }
                
PAGE_ACCESS_TOKEN = 'EAAgZCpzUtPzEBACMtZCJsjqBlfe2ne0u7G9ofnstbuIc719JiuRt2VYdhhYhJPkKSivXyL6BH2jzVOpDC7epbuHNjPLXL0PbDCh0LyVfuIkqFGPiIMPmZC2dyL2UCAaDiNe3X8iuoZAnfMifE96XoF3iSj6Ntvo9uca8WHq0BrY50nxahrqj'#texty
# PAGE_ACCESS_TOKEN='EAAKDDnoBSygBAAN02M1gZB9ikgWxnRtZB67EjAyYpQ9qOpAIutHMZBaZBRHEGwWyvlLo5ksdC9EBZBROENQZCeNvLZBYYnICjcUaXatFf9aynZBbLWi6ZCcItzegN2skv4P26FIUUJSJGDtp5EOkcSSmJPGmv8RuWZCrZByZCjpzZBDNxKwZDZD'#HH TEST SHOP

# PAGE_ACCESS_TOKEN='EAAKDDnoBSygBAI7RbVqTDoMPAl2F0cXvxzEFuUFxZCIdel5RGmEANN4sisCOkp0DFaa5MSZAZBYCLs0y39x9BKZCqZCYPdnNUzWtiiWnGZCcLh7YQVbYsaMECEMbWcp2xvOMNIKB5KzIqmGhnLw5euU4VfmL1tOpXqoREELv4UBgZDZD' #Xtive

def send_message(text, recipient_id, pid):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': page_token[str(pid)]
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

def get_bot_response(message, sender, receiver):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    #return "This is the data received:\n{}".format(message)
    url = 'https://phai-message-test.herokuapp.com/message'
    data= {
        'content': message ,
        'sender_id': sender,
        'receiver_id': receiver,
    }
    req = requests.post(url, data = data)
    text = json.loads(req.text)
    print(text)
    return text['content']

#localhost:1337/webhook?hub.verify_token=<YOUR_VERIFY_TOKEN>&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe
def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(message, sender, page_id):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    dialogflow_msg = get_bot_response(message, sender, page_id)
    print(dialogflow_msg)
    send_message(dialogflow_msg, sender, page_id)
    
# respond(message, sender, page_id)
# send_message(text, recipient_id, pid)
# get_bot_response(message, sender, receiver)

def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

# =============================================================================
# 
# 2019-10-24T05:57:48.917798+00:00 app[web.1]: { sender: { id: '2494452660649366' },
# 2019-10-24T05:57:48.917845+00:00 app[web.1]:   recipient: { id: '105637970864675' },
# 2019-10-24T05:57:48.917847+00:00 app[web.1]:   timestamp: 1571896668328,
# 2019-10-24T05:57:48.917849+00:00 app[web.1]:   read: { watermark: 1571896661318 } }
# =============================================================================


@app.route("/webhook",methods=['GET','POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                recipient_id = x['recipient']['id']
                try:
                    respond(message=text, sender=sender_id, page_id=recipient_id)
                except Exception as e:
                    print ("error in level argument",e)

        return "ok"
       
# @app.route('/webhook', methods=['GET', 'POST'])
# def home():
#     if request.method == 'GET':
    
#         app.logger.info('Headers: %s', request.headers)
#         app.logger.info('Body: %s', request.get_data())
#         return verify_webhook(request)

#     if request.method == 'POST':
#         payload = request.json
#         req = request.get_json(silent=False)
#         print(req)
#         # app.logger.debug('Headers: %s', request.headers)
#         log = app.logger.debug('Body json: %s', request.json)
#         # app.logger.debug('Body')
#         # app.logger.debug('Body: %s', request.get_data())
#         # app.logger.debug('Body parse form: %s', request.get_data(parse_form_data=True))
#         # app.logger.debug('Body form: %s', request.form)
#         # app.logger.debug('Body form dict: %s', request.form.to_dict(flat=False))
#         # event = payload['entry'][0]['messaging']
#         # pid = payload['entry'][0]['id']
#         # for x in event:
#             # if is_user_message(x):
#                 # text = x['message']['text']
#         lineNotify(str(request.json),line_token)
#         return "ok"
        
if __name__ == '__main__':

    app.run(host= '0.0.0.0', debug=True, port=8123)
