""" Server module for the coffee shop application. """

from socket import *
from threading import *
from reports import *
from orders import save_order


class ClientThread(Thread):
    def __init__(self, client_socket, client_address):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address

        # Create an RLock object to lock the threads when they are accessing the files
        self.rlock = RLock()

        self.connection_status = None
        self.login_status = None

        self.send_message("connectionsuccess")
        self.connection_status = 1

    # This method is called when the thread is started
    def run(self):
        # The server will receive the username and password from the client and check if the user is in the users.txt file
        while self.connection_status == 1:
            try:
                _, username, password = self.receive_message().split(";")
            except ValueError:
                self.client_socket.close()
                self.connection_status = 0
                print("The client from {} is disconnected.".format(
                    self.client_address))
                break

            role = self.login(username, password)

            # If the user is not in the users.txt file, the server will send a login failure message to the client
            if self.login_status == 0:
                self.send_message("loginfailure")

            else:
                while self.login_status == 1:
                    # If the user is a barista, the server will receive the order from the client and save it to the orders.txt file
                    if role == "barista":
                        client_message = self.receive_message()
                        if client_message == "connectionclosed":
                            self.client_socket.close()
                            self.connection_status = 0
                            print("The client from {} is disconnected.".format(
                                self.client_address))
                            break
                        else:
                            self.rlock.acquire()
                            server_message = save_order(client_message)
                            self.rlock.release()
                            self.send_message(server_message)

                    # If the user is a manager, the server will receive the report name from the client and send the report to the client
                    elif role == "manager":
                        reports = {"report1": report1(), "report2": report2(
                        ), "report3": report3(), "report4": report4()}
                        client_message = self.receive_message().split(";")
                        if client_message[0] == "connectionclosed":
                            self.client_socket.close()
                            self.connection_status = 0
                            print("The client from {} is disconnected.".format(
                                self.client_address))
                            break
                        else:
                            report_name = client_message[0]
                            report = reports[report_name]
                            self.send_message(report)

    # Method to check if the client is disconnected
    def is_disconnected(self):
        return self.connection_status == 0

    # Login method to check if the user is in the users.txt file
    def login(self, username, password):
        with open("users.txt", "r") as file:
            for line in file:
                line = line.split(";")
                if username == line[0] and password == line[1]:
                    role = line[2].strip()
                    self.login_status = 1

                    server_message = "loginsuccess;{};{}".format(
                        username, role)
                    self.send_message(server_message)
                    return role
                else:
                    self.login_status = 0

    # Method to send messages to the client
    def send_message(self, message):
        self.client_socket.send(message.encode())

    # Method to receive messages from the client
    def receive_message(self):
        return self.client_socket.recv(1024).decode()


# Server function to create a server socket and listen for clients
def server():
    TCP_IP = "localhost"
    TCP_PORT = 7777

    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((TCP_IP, TCP_PORT))
    print("Server is running...")
    server.listen(5)
    print("Server is waiting for clients...")
    while True:
        client_socket, client_address = server.accept()
        print("A client has connected to the server from", client_address)
        new_client_thread = ClientThread(client_socket, client_address)
        new_client_thread.start()
        if new_client_thread.is_disconnected():
            del new_client_thread
            break


if __name__ == "__main__":
    server()
