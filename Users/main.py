# Imports
import requests
import json
from pathlib import Path

# Establishing the files
path = Path(__file__).with_name('users.txt')
usersFile = path.open('r')
config_path = Path(__file__).with_name('config.json')
config = config_path.open('r')
config = json.loads(config.read())
on_file = open("on.txt", "w+")
off_file = open("off.txt", "w+")
contents = usersFile.read().splitlines()

# Creating session
rblx_session = requests.Session()
rblx_session.cookies[".ROBLOSECURITY"] = config["Cookie"]

def http_request(send_method, url, **args):
    request = rblx_session.request(send_method, url, **args)

    if "X-CSRF-TOKEN" in request.headers:
        if "errors" in request.json():
            if request.json()["errors"][0]["message"] == "Token Validation Failed":
                rblx_session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
                request = rblx_session.request(send_method, url, **args)    

    return request

def get_user_id(line):
    if line.isdigit():
        return line
    else:
        try:
            search_query = http_request("get", "https://api.roblox.com/users/get-by-username?username=" + str(line))

            if search_query.ok:
                user = json.loads(search_query.content)

                userId = user['Id']

                return userId
        except:
            print("Search query error: " + str(search_query.status_code))

def get_user_name(line):
    if line.isdigit():
        user_request = http_request("get", f"https://users.roblox.com/v1/users/{line}")

        if user_request.ok:
            data = json.loads(user_request.content)

            return data['name']
    else:
        return line

for line in contents:
    userId = get_user_id(line)

    if userId:
        # Seeing if they have messages open
        #can_message = http_request("get", url = f"https://privatemessages.roblox.com/v1/messages/{userId}/can-message")
        can_message = http_request("get", url = "https://www.roblox.com/users/profile/profileheader-json", params = {"userId": userId})

        if can_message.ok:
            can_message = json.loads(can_message.content)['CanMessage']

            user_name = get_user_name(line)

            if can_message:
                on_file.write(f"{user_name} \n")
            else:
                off_file.write(f"{user_name} \n")
    
# Closing the files after we are done with them
usersFile.close()
on_file.close()
off_file.close()
