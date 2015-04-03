import tkinter as tk
from tkinter.scrolledtext import ScrolledText
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
            data = pickle.loads(data)
            print(data)
            write_to(text_out, data)
        else:
            break

def write_to(dest, msg):
    #dest.update_idletasks()
    #scrolled_down = dest.bbox(tk.END) is not None
    #print(dest.bbox(tk.END))
    dest.configure(state='normal')
    dest.insert(tk.END, msg + '\n')
    dest.configure(state='disabled')
    #if scrolled_down:
    #   print(scrolled_down)
    dest.see(tk.END)

def main():
    global text_in
    global text_out
    global sock

    HOST = 'arctem.com'
    HOST = 'localhost'
    PORT = 50001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    t = threading.Thread(target=socket_thread, args=(sock,))
    t.start()

    window = tk.Tk()

    text_out = ScrolledText(window, state='disabled', takefocus=0)
    #text_out.configure(state='disabled')
    text_out.pack()

    text_in = tk.Entry(window, takefocus=1)
    text_in.bind("<Return>", evaluate_in)
    text_in.pack()

    window.mainloop()

if __name__ == '__main__':
    main()
