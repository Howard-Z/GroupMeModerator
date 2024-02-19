from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import os
from dotenv import load_dotenv
import argparse

load_dotenv()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, world!")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Decode the post data
        post_data_decoded = post_data.decode('utf-8')

        # Parse the JSON data
        try:
            json_data = json.loads(post_data_decoded)
            # Print the parsed JSON data
        except json.JSONDecodeError as e:
            # If JSON parsing fails, print an error message
            print("failed to decode")
        print(json_data['text'])
        for word in Moderator.black_list:
            if word in json_data['text']:
                sender_id = json_data['sender_id']
                group_id = json_data['group_id']
                userid = Moderator.get_userid(group_id, sender_id)
                Moderator.kick(group_id, userid)
                Moderator.say_funny()



def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

class Moderator():
    token = None
    id = None
    black_list = None
    def __init__(self, blacklist_path, api_token, bot_id):
        Moderator.token = api_token
        Moderator.id = bot_id
        #TODO Process the blacklist
        self.process_blacklist(blacklist_path)

    def process_blacklist(self, path):
        f = open(path, "r")
        Moderator.black_list = set()
        for word in f:
            Moderator.black_list.add(word)


    @staticmethod
    def get_userid(groupid, sender_id):
        url = f"{base_url}groups/{groupid}?token={token}"
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        json_data = response.json()
        memberlist = json_data['response']['members']
        for member in memberlist:
            if member['user_id'] == sender_id:
                return member['id']


    @staticmethod
    def kick(groupid, userid):
        url = f"{base_url}groups/{groupid}/members/{userid}/remove?token={token}"
        print(url)
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"User {userid} successfully kicked from group {groupid}")
            return True
        else:
            print(f"Failed to kick user {userid} from group {groupid}. Status code: {response.status_code}")
            return False
        
    @staticmethod
    def say_funny():
        message = "get sh!t on"
        url = "https://api.groupme.com/v3/bots/post"
        data = {
            "text": message,
            "bot_id": id
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")


if __name__ == '__main__':

    # Creating argument parser for the command line
    parser = argparse.ArgumentParser(description="GroupMe Moderator for BCT")
    parser.add_argument("--token", required=True, help="The api token to be used.")
    parser.add_argument("--id", required=True, help="The bot id to be used.")
    parser.add_argument("--file", required=True, help="The blacklist file path to be used.")

    args = parser.parse_args()

    # Accessing the arguments
    token = args.token
    id = args.id
    file_path = args.file
    
    base_url = "https://api.groupme.com/v3/"

    bot = Moderator(file_path, token, id)

    run()