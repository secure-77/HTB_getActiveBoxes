import json
import requests
import re


settings_file = '.settings.json'
use_proxy = False

htb_login_enpoint = 'https://www.hackthebox.com/api/v4/login'
htb_list_endpoint = 'https://www.hackthebox.com/api/v4/machine/list'

http_proxy  = "http://127.0.0.1:8080"
myproxies = { "https" : http_proxy }


headers = {"Host":"www.hackthebox.com", "User-Agent":"python script","Accept": "application/json"}


def get_creds():
    print("[+] reading settings...")
    with open(settings_file, 'r') as file:
        data = file.read()
    settings_data = json.loads(data)
    global login_data
    global gitignore_file
    login_data = settings_data.get('creds')
    gitignore_file = settings_data.get('git_ignore')

    
def get_token():
    global token
    print("[+] connecting to HTB...")
    
    if use_proxy:
        requests.packages.urllib3.disable_warnings() 
        response = requests.post(htb_login_enpoint, headers=headers, json=login_data, proxies=myproxies, verify=False)
    else:
        response = requests.post(htb_login_enpoint, headers=headers, json=login_data)

    print("[+] login and request access token..")
    json_data = json.loads(response.text)
    token = json_data.get('message').get('access_token')
    if token: print("[+] token successfull received..")
    #print(token)
    

def get_active_boxes():
    print("[+] request active boxes...")
    global headers
    headers['Authorization'] = 'Bearer ' + token
    if use_proxy:
        requests.packages.urllib3.disable_warnings() 
        response = requests.get(htb_list_endpoint, headers=headers, proxies=myproxies, verify=False)
    else:
        response = requests.get(htb_list_endpoint, headers=headers)

    global box_infos
    box_infos = json.loads(response.text)
    #print(box_infos)
    print("[+] received active boxes...")



def update_gitignore():
    activeBoxes = "\n"

    for box in box_infos.get('info'):
        boxname = box.get('name')
        activeBoxes =activeBoxes + "WriteUps/HackTheBox/" + str(boxname) + '\n'

    print("[+] update gitignore list...")
    with open(gitignore_file, 'r') as file:
        data = file.read()

    data = re.sub(r"(# Active Boxes START)(\n.*)*(# Active Boxes END)", r"\1"+activeBoxes+r"\3", data)

    with open(gitignore_file, 'w') as file:
        file.write(data)



get_creds()
get_token()
get_active_boxes()
update_gitignore()

print("[+] done")



