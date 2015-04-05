import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import socket
import pickle
import threading

def evaluate_in(event, text_in, text_out):
    text = text_in.get()
    print(text)
    sock.sendall(pickle.dumps(text))
    write_to(text_out, text.upper())
    text_in.delete(0, tk.END)

def socket_thread(sock, text_out):
    pickle_separator = b'q\x00.'

    while True:
        data = sock.recv(1024)
        if not data:
            break

        data = data.split(pickle_separator)
        for datum in data:
            if datum == b'':
                continue
            datum = (datum + pickle_separator)
            datum = pickle.loads(datum)
            write_to(text_out, datum)

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
    global sock


    window = tk.Tk()

    text_out = ScrolledText(window, state='disabled', takefocus=0)
    #text_out.configure(state='disabled')
    text_out.pack()

    text_in = tk.Entry(window, takefocus=1)
    text_in.bind("<Return>", lambda e: evaluate_in(e, text_in, text_out))
    text_in.pack()


    HOST = 'arctem.com'
    HOST = 'localhost'
    PORT = 50001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    t = threading.Thread(target=socket_thread, args=(sock, text_out))
    t.start()

    window.mainloop()

if __name__ == '__main__':
    main()
