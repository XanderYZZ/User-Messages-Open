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
contents = usersFile.read()

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

for line in contents.split():
    search_query = http_request("get", "https://users.roblox.com/v1/users/search?keyword=" + line + "&limit=10")

    if search_query.ok:
        user = search_query.json()['data'][0]

        userId = user['id']

        # Seeing if they have messages open
        can_message = http_request("get", url = f"https://privatemessages.roblox.com/v1/messages/{userId}/can-message")

        if can_message.ok:
            can_message = json.loads(can_message.content)['canMessage']

            if can_message:
                on_file.write(f"{line} \n")
            else:
                off_file.write(f"{line} \n")
    else:
        print("Search query error: " + str(search_query.status_code))

# Closing the files after we are done with them
usersFile.close()
on_file.close()
off_file.close()