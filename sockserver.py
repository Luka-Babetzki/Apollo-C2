import socket
import sys

def banner():
    print('                       _ _          _____ ___   ')     
    print('     /\               | | |        / ____|__ \  ')      
    print('    /  \   _ __   ___ | | | ___   | |       ) | ')
    print('   / /\ \ |  _ \ / _ \| | |/ _ \  | |      / /  ')
    print('  / ____ \| |_) | (_) | | | (_) | | |____ / /_  ')
    print(' /_/    \_\ .__/ \___/|_|_|\___/   \_____|____| ')
    print('          | |                                   ')
    print('          |_|               By Luka Babetzki    ')             


def comm_in(remote_target):
    print('[+] Awaiting response...')
    response = remote_target.recv(1024).decode()
    return response

def comm_out(remote_target, message):
    remote_target.send(message.encode())

def listener_handler():
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    remote_target, remote_ip = sock.accept()
    comm_handler(remote_target, remote_ip)

def comm_handler(remote_target, remote_ip):
    print(f'[+] Connection received from: {remote_ip[0]}')
    while True:
        try:
            message = input('Message to send#>')
            if message == 'exit':
                remote_target.send(message.encode())
                remote_target.close()
                break
            remote_target.send(message.encode())
            response = remote_target.recv(1024).decode()
            if response == 'exit':
                print('[-] The client has terminated the session.')
                remote_target.close()
                break
            print(response)
        except KeyboardInterrupt:
            print('\n[+] Keyboard interrupt issued.')
            message = 'exit'
            remote_target.send(message.encode())
            sock.close()
            break
        except Exception:
            remote_target.close()
            break

if __name__ == '__main__':
    banner()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
        listener_handler()
    except IndexError:
        print('[-] Command line arguement(s) missing. Please specify IP and Port.')
    except Exception as e:
        print(e)
