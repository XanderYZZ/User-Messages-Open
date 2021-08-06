# Imports
import requests
import json
from pathlib import Path

# Establishing the files
path = Path(__file__).with_name('users.txt')
usersFile = path.open('r')
on_file = open("on.txt", "w+")
off_file = open("off.txt", "w+")
contents = usersFile.read()

# Creating session
COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_E4374764BDD396D8A628A01189D40B00868E040CDB6F46A349999D1B0EB62BD86AE6A81D2155BE8953951444C3DFC25B69C7DAEDC14603B1945C6224C0FCE833EB51D02595C9D9DE4D27D5067569A18310CB0B6BEB6ABD070D0B51B7B9615A8B16124F5BDA9EC2F930B068AD8161AE970310DFB018D4D4D12E8D6608884B7C0E3092351E3178DB213B211894F2DB79F1D446FE49AC515791497765B80D35C1ED94B9AFC5E1C449B924153854865A4EE6AD77FF09B5182854D54ADC7980C7AA5CB3D02A407E8BDD7618E0F0A06A5A8C8020EFD315FCEFA5BFF6CC5458F1119830386549347BEC511B08E65F889AF971680A71F7AF4AB65B88625CA0F7E5A031684D5E7C22199959EBF49BCB5A017CD8B6416797F877E8C3B1086AD74D59BA54B138B337D81B01F9158551B8C9C57624257B429BBC73D5957CD7D3B73A4E4ED309F6E27BCA"
rblx_session = requests.Session()
rblx_session.cookies[".ROBLOSECURITY"] = COOKIE

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