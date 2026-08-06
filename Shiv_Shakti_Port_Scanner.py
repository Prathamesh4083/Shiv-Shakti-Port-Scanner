import socket
import tkinter as tk
from tkinter import scrolledtext
import threading
from queue import Queue

# Known services dictionary
services = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 8080: "HTTP-Alt"
}

queue = Queue()
NUM_THREADS = 150   # Speed controller


def scan_port(target):
    while not queue.empty():

        port = queue.get()

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)

            result = sock.connect_ex((target, port))

            if result == 0:
                service = services.get(port, "Unknown")

                output_box.insert(
                    tk.END,
                    f"Port {port} OPEN → {service}\n"
                )

            sock.close()

        except:
            pass

        queue.task_done()


def start_scanning():

    target = ip_entry.get()

    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except:
        output_box.insert(tk.END, "Invalid Port Range!\n")
        return

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Scanning Target: {target}\n\n")

    # Add ports into queue
    for port in range(start_port, end_port + 1):
        queue.put(port)

    # Create worker threads
    for _ in range(NUM_THREADS):
        thread = threading.Thread(
            target=scan_port,
            args=(target,)
        )
        thread.daemon = True
        thread.start()

    queue.join()

    output_box.insert(tk.END, "\nScan Completed Successfully!")


def run_thread():

    threading.Thread(
        target=start_scanning
    ).start()

def clear_screen():
    output_box.delete(1.0,tk.END)
    
# GUI WINDOW
root = tk.Tk()
root.title("Shiva-Shakti Port Scanner")
root.geometry("600x550")
# Target IP
tk.Label(root, text="Enter Target IP",bg="white",fg="black", font=("Arial", 12)).pack()

ip_entry = tk.Entry(root, font=("Arial", 12), width=30, bg="violet", fg="white")
ip_entry.pack()
ip_entry.pack(pady=5)


# Port Range Frame
frame = tk.Frame(root)
frame.pack()

tk.Label(frame,text="Start Port").grid(row=0, column=0)

start_port_entry = tk.Entry(frame, width=10)
start_port_entry.insert(0, "1")
start_port_entry.grid(row=0, column=1)


tk.Label(frame,text="End Port").grid(row=0, column=2)

end_port_entry = tk.Entry(frame, width=10)
end_port_entry.insert(0, "1024")
end_port_entry.grid(row=0, column=3)


# Scan Button
scan_btn = tk.Button(root, text="Start Scan",bg="green", fg="white", font=("Arial", 12),command=run_thread)

scan_btn.pack(pady=10)

# Clear Button
clear_btn = tk.Button(root,text="Clear",bg="Yellow", fg="Red" , font=("Arial", 12),
command=clear_screen )

clear_btn.pack(pady=12)

# Output Box
output_box = scrolledtext.ScrolledText(root, width=70, height=25,font=("Consolas", 10))

output_box.pack()

root.mainloop() # For Infinite Run of my code
