""" This module contains the client class, which is the GUI for the client. """

from socket import *
from tkinter import *
from tkinter import messagebox
from baristapanel import BaristaPanel
from managerpanel import ManagerPanel


class Client(Frame):
    def __init__(self, client_socket):
        self.client_socket = client_socket

        server_message = self.receive_message()
        if server_message == "connectionsuccess":
            # Create the GUI for the client
            Frame.__init__(self)
            self.master.title("Login")
            self.pack(side=TOP)

            self.frame1 = Frame(self)
            self.frame1.pack(padx=5, pady=5)

            self.username_label = Label(self.frame1, text="User name")
            self.username_label.pack(side=LEFT, padx=5, pady=5)

            self.username = Entry(self.frame1, name="username")
            self.username.pack(side=LEFT, padx=5, pady=5)

            self.frame2 = Frame(self)
            self.frame2.pack(padx=5, pady=5)

            self.password_label = Label(self.frame2, text="Password")
            self.password_label.pack(side=LEFT, padx=5, pady=5)

            self.password = Entry(self.frame2, name="password", show="*")
            self.password.pack(side=LEFT, padx=5, pady=5)

            self.frame3 = Frame(self)
            self.frame3.pack(padx=5, pady=5)

            # Create the login button
            self.login_button = Button(
                self.frame3, text="Login", command=self.login_button_pressed)
            self.login_button.pack(side=LEFT, padx=5, pady=5)
        else:
            messagebox.showerror("Connection Error", "connectionfailed")

    # This method is called when the login button is pressed
    def login_button_pressed(self):
        username = self.username.get()
        password = self.password.get()

        # Check if the username and password are not empty
        if username == "" or password == "":
            messagebox.showerror(
                "Login Error", "Please enter a username and password")
            return

        client_message = "login;{};{}".format(username, password)
        self.send_message(client_message)

        server_message = self.receive_message().split(";")

        if server_message[0] == "loginsuccess":
            role = server_message[2]
            # Create the appropriate panel for the user
            if role == "barista":
                panel = BaristaPanel(username, self.client_socket)
                self.destroy()
                panel.tkraise()
            elif role == "manager":
                panel = ManagerPanel(username, self.client_socket)
                self.destroy()
                panel.tkraise()
        else:
            messagebox.showerror("Login Error", server_message)

    # Method to send a message to the server
    def send_message(self, message):
        self.client_socket.send(message.encode())

    # Method to receive a message from the server
    def receive_message(self):
        return self.client_socket.recv(1024).decode()


# Client function to create the client socket to connect to the server and create the client GUI
def client():
    HOST = "localhost"
    PORT = 7777

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    screen = Client(client_socket)
    screen.mainloop()


if __name__ == "__main__":
    client()
