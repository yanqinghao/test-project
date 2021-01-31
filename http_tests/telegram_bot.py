import requests

send_message_url = 'https://api.telegram.org/bot<token>/sendMessage'
updates_url = 'https://api.telegram.org/bot<token>/getUpdates'

token = open('private/bot_token').readline()
send_message_url = send_message_url.replace('<token>', token)
updates_url = updates_url.replace('<token>', token)

chat_id = open('private/chat_id').readline()
data = {"chat_id": int(chat_id), "text": "test message"}

r = requests.post(send_message_url, data=data)

print(r.content)
