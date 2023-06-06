#!/usr/bin/env python
import json
import time
from flask import Flask, request
import requests
import logging

message = "Текст который должен прислать бот"
client_id = ""
client_secret = ""
user_id = ""
token = requests.post("https://api.avito.ru/token", params={"client_id": f"{client_id}", "client_secret": f"{client_secret}", "grant_type": "client_credentials"})
headers = {"Authorization": f"Bearer {token.json()['access_token']}"}
print(headers)

app = Flask(__name__)

def get_user_id(id_chat: str):
    print("Вызвана функция получить пользователя")
    try:
        if id_chat == "u2i-A6NeEsowoLVhlRb3kVD4Ug":
            return True
        with open("users.txt", mode="r+") as file:
            text_in_file = file.read().split("\n")
            if id_chat in text_in_file:
                return False
            else:
                file.writelines(f"{id_chat}\n")
                return True
    except:
        return True


@app.route("/", methods=["POST", "GET"])
def main():
    print("Вызвана функция main")
    print(request.json)
    avito_request = request.json["payload"]["value"]
    chat_id = avito_request["chat_id"]
    last_message_user_id = avito_request["author_id"]
    response = {
  "message": {
    "text": f"{message}"
  },
  "type": "text"
}
    logging.debug(request.json)

    if last_message_user_id != int(user_id) and get_user_id(str(chat_id)):
        mail = requests.post(f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages",
                             headers=headers,
                             data=json.dumps(response))
        logging.debug(mail)
    return ""


if __name__ == "__main__":
    app.run(debug=True, host="", port=5000)
