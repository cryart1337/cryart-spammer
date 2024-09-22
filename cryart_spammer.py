# CRYART SPAMMER - 22.04.2024
# CRYART SPAMMER - V1.0

try:
    import requests
    import time
    from datetime import datetime, timezone
    import socket
    import sys
    import fade
    import pathlib
    import os
    import random
    import threading
    import ctypes
except ImportError as e:
    import subprocess
    import sys
    
    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
    requirements = ['requests', 'datetime', 'fade']
    for pkg in requirements:
        try:
            __import__(pkg)
        except ImportError:
            print(f"Installing {pkg}...")
            install(pkg)
            
    with open('requirements.txt', 'w') as f:
        for requirement in requirements:
            f.write(requirement + '\n')

log_file = open("spammer.log", "w")

pulamea = r"""

 ██████╗██████╗ ██╗   ██╗ █████╗ ██████╗ ████████╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗╚══██╔══╝
██║     ██████╔╝ ╚████╔╝ ███████║██████╔╝   ██║   
██║     ██╔══██╗  ╚██╔╝  ██╔══██║██╔══██╗   ██║   
╚██████╗██║  ██║   ██║   ██║  ██║██║  ██║   ██║   
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  
"""
pulamea2 = r"""
███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
"""

def style_cmd():
    # remove maximize button
    GWL_STYLE = -16
    WS_MAXIMIZEBOX = 0x00010000
    
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    style &= ~WS_MAXIMIZEBOX
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
    ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x03 | 0x40)

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def print_start(text):
    text = fade.purplepink(text)
    sys.stdout.write(text)
    sys.stdout.flush()

def colorize(text, color):
    colors = {
        'red': '31',
        'green': '32',
        'blue': '34',
    }
    reset = '0'
    color = colors.get(color, '37')
    return f"\033[{color}m{text}\033[{reset}m"

def log(type, message):
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    draq = f"{timestamp} {type}: {message}\n"
    if type == 'INFO':
        draq2 = colorize(draq, 'green')
    elif type == 'ERROR':
        draq2 = colorize(draq, 'red')
    elif type == 'CRITICAL':
        draq2 = colorize(draq, 'blue')
    else:
        draq2 = draq
    print(draq2, end="")
    log_file.write(draq)
    log_file.flush()

def check_internet_connection():
    host = 'www.google.com'
    port = 80
    timeout = 5
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False
    
def get_tokens():
    with open('tokens.txt', 'r') as file:
        tokens = file.readlines()
        tokens = [token.strip() for token in tokens]
    return tokens

def validate_token(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if response.status_code == 200:
            return True, 'valid'
        else:
            return False, response.status_code
    except Exception as e:
        return False, e
    
def get_username(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if response.status_code == 200:
            return response.json()['username']
        else:
            return None
    except Exception as e:
        return None
    
def get_channel(token, channel_id):
    url = f'https://discord.com/api/v10/channels/{channel_id}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['name']
    else:
        return None
    

headers = {
    'Content-Type': 'application/json'
}
session = requests.Session()

def send_message(token, channel_id, message):
    global tokens
    headers['Authorization'] = token
    data = {
        'content': message
    }
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
    url2 = f'https://discord.com/api/v10/channels/{channel_id}/typing'
    
    try:
        session.post(url2, headers=headers)
        response = session.post(url, json=data)
        if response.status_code == 200:
            pass
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After'))
            log("ERROR", f"Rate limit on {get_username(token)} ({tokens.index(token)})...")
            time.sleep(retry_after)
            send_message(token, channel_id, message)
        else:
            log("ERROR", f"Failed to send message ({response.status_code})")
    except Exception as e:
        log("CRITICAL", e)
        
options = "1. Spam on token\n2. Spam on all tokens\n3. Show all tokens"

def status(token):
    url = f"https://discord.com/api/v9/users/@me/settings"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    sal = random.choice(["#EEK ON TOP", "CRYART SPAMMER", "#EEK", "MADE BY CEEK", "MADE BY CRYART", "Fecior treci la lupta"])
    data = {
        'status': random.choice(['online', 'idle', 'dnd']),
        'custom_status': {
            'text': sal,
            'emoji_name': '👹',
            'emoji_id': None
        }
    }
    requests.patch(url, headers=headers, json=data)
    
def status_loop(token, interval=15):
    while True:
        status(token)
        time.sleep(interval)
        
def status_thread(token, interval=15):
    thread = threading.Thread(target=status_loop, args=(token, interval))
    thread.daemon = True
    thread.start()
    
def show_readme():
    try:
        with open("README.txt", "r") as file:
            message = file.read()
        return message
    except FileNotFoundError:
        with open("README.txt", "w") as file:
            message = """\
*********************************************
*                THANKS FOR BUYING!         *
*                                           *
*          CRYART SPAMMER v1.0              *
*                04.06.2024                  *
*********************************************"""
            file.write(message)
        return message

def spam_on_token(token_list):
    while True:
        tkn = int(input(colorize('Token number (choice number 3 to get tokens): ', 'blue')))
        token = token_list.get(tkn)
        if token:
            break
        else:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            sys.stdout.flush()
    while True:
        response = input(colorize('Notepad filename (if is in other directory specify it): ', 'blue'))
        if response.lower() in ['yes', 'y']:
            status_thread(token)
            break
        elif response.lower() in ['no', 'n']:
            break
        else:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            sys.stdout.flush()
    while True:
        notepad = input(colorize('Notepad filename (if is in other directory specify it): ', 'blue'))
        notepad2 = pathlib.Path(notepad)
        if not notepad2.is_file():
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            sys.stdout.flush()
        else:
            try:
                with open(notepad2, 'r', encoding='utf-8') as file:
                    lines = [line.strip() for line in file if line.strip()]
                    if not lines:
                        sys.stdout.write('\033[F')
                        sys.stdout.write('\033[K')
                        sys.stdout.flush()
                        log("ERROR", "The notepad is empty. Please choose another notepad.")
                    else:
                        break
            except Exception as e:
                log("ERROR", e)
                input('')
                sys.exit()
    channel_id = int(input(colorize('Channel id: ', 'blue')))
    delay = float(input(colorize('Delay (in seconds): ', 'blue')))
    check = get_channel(token, channel_id)
    
    if check:
        send_message(token, channel_id, f"```{show_readme()}```")
        log("INFO", f"Start spamming on {check}...")
        k = 0
        for line in lines:
            send_message(token, channel_id, line.strip())
            time.sleep(delay)
            k += 1
        
        log("INFO", f"Finish spamming {k} lines")
        log("INFO", "Press enter to exit...")
        input('')
        sys.exit()
        
    else:
        log("ERROR", f"Invalid channel id ({channel_id})")
        input('')
        sys.exit()

def spam_on_all_tokens(token_list):
    while True:
        notepad = input(colorize('Notepad filename (if is in other directory specify it): ', 'blue'))
        notepad2 = pathlib.Path(notepad)
        if not notepad2.is_file():
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            sys.stdout.flush()
        else:
            try:
                with open(notepad2, 'r', encoding='utf-8') as file:
                    lines = [line.strip() for line in file if line.strip()]
                    if not lines:
                        sys.stdout.write('\033[F')
                        sys.stdout.write('\033[K')
                        sys.stdout.flush()
                        log("ERROR", "The notepad is empty. Please choose another notepad.")
                    else:
                        break
            except Exception as e:
                log("ERROR", e)
                input('')
                sys.exit()
    while True:
        response = input(colorize("Do you want to dislay custom status? (yes/no): ", 'blue'))
        if response.lower() in ['yes', 'y']:
            for token in token_list.values():
                status_thread(token)
            break
        elif response.lower() in ['no', 'n']:
            break
        else:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            sys.stdout.flush()
    channel_id = int(input(colorize('Channel id: ', 'blue')))
    delay = float(input(colorize('Delay (in seconds): ', 'blue')))
    
    for token in token_list.values():
        check = get_channel(token, channel_id)
    
        if check:
            send_message(token, channel_id, f"```{show_readme()}```")
            log("INFO", f"Start spamming on {check}...")
        
        else:
            log("ERROR", f"Invalid channel id ({channel_id})")
            input('')
            sys.exit()
    
    k = 0
    for line in lines:
        for token in token_list.values():
            send_message(token, channel_id, line.strip())
            if delay != 0:
                time.sleep(delay)
            k += 1
        
    log("INFO", f"Finish spamming {k} lines")
    log("INFO", "Press enter to exit...")
    input('')
    sys.exit()
    
def show_tokens(tokens):
    print(colorize('Tokens: ', 'blue'))
    for idx, token in tokens.items():
        print(colorize(f"{idx}: {token}", 'blue'))

def readme():
    message = show_readme()
    print(fade.brazil(message))
    time.sleep(3)
    clear()
    
def main():
    print_start(f"\t\t\t {pulamea}")
    print_start(f"\t\t\t {pulamea2}")
    print('\n')
    if check_internet_connection():
        log("INFO", "Good internet connection detected")
    else:
        log("ERROR", "Bad internet connection detected")
        log("ERROR", "Press enter to exit...")
        input('')
        sys.exit()
    mata = get_tokens()
    valid, invalid = 0, 0
    tokens = {}
    for idx, token in enumerate(mata, start=1):
        tkn, message = validate_token(token)
        if tkn is True:
            valid += 1
            tokens[idx] = token
        else:
            if message == 401:
                invalid += 1
            else:
                log("ERROR", message)
    log('INFO', f"{valid} valid tokens, {invalid} invalid tokens \n")
    if valid == 0:
        log("CRITICAL", "No valid tokens found")
        log("CRITICAL", "Press enter to exit...")
        input('')
        sys.exit()
    else:
        print('\n')
        sys.stdout.write(fade.water(options))
        sys.stdout.flush()
        while True:
            response = input(colorize("Enter your choice: ", 'blue'))
            if response in ['1', '2', '3']:
                if response == '1':
                    spam_on_token(tokens)
                elif response == '2':
                    spam_on_all_tokens(tokens)
                elif response == '3':
                    show_tokens(tokens)
                break
            else:
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
                sys.stdout.flush()

if __name__ == '__main__':
    style_cmd()
    clear()
    readme()
    main()