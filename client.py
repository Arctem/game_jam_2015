import tkinter as tk
import socket
import pickle
import threading

def evaluate_in(event):
    text = text_in.get()
    print(text)
    sock.sendall(pickle.dumps(text))
    text_in.delete(0, tk.END)

def socket_thread(sock):
    while True:
        data = sock.recv(1024)
        if data:
            print(pickle.loads(data))
        else:
            break

def main():
    global text_in
    global sock

    HOST = 'arctem.com'
    HOST = 'localhost'
    PORT = 50001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    t = threading.Thread(target=socket_thread, args=(sock,))
    t.start()

    window = tk.Tk()

    text_out = tk.Text(window)
    text_out.pack()

    text_in = tk.Entry(window)
    text_in.bind("<Return>", evaluate_in)
    text_in.pack()

    window.mainloop()

if __name__ == '__main__':
    main()
