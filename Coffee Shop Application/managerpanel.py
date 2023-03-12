""" This module contains the ManagerPanel class, which is the GUI for the manager. """

from tkinter import *
from tkinter import messagebox
from socket import *


class ManagerPanel(Frame):
    def __init__(self, manager, client_socket):
        self.manager = manager
        self.client_socket = client_socket

        # Create the GUI for the manager
        Frame.__init__(self)
        self.master.title("Manager Panel")
        self.pack()

        self.reports_frame = Frame(self)
        self.reports_frame.pack(padx=5, pady=5, side=TOP)
        self.reports_label = Label(self.reports_frame, text="REPORTS")
        self.reports_label.pack(side="top")

        # Report questions to be displayed on the GUI
        questions = ["(1) What is the most popular coffee overall?", "(2) Which barista has the highest number of orders?",
                     "(3) What is the most popular product for the orders with the discount code?", "(4) What is the most popular cake that is bought with expresso?"]

        # Radio buttons for the report questions
        self.report_name = StringVar()
        self.report_name.set("report1")

        self.q1_button = Radiobutton(
            self.reports_frame, text=questions[0], variable=self.report_name, value="report1")
        self.q1_button.pack(anchor="w")

        self.q2_button = Radiobutton(
            self.reports_frame, text=questions[1], variable=self.report_name, value="report2")
        self.q2_button.pack(anchor="w")

        self.q3_button = Radiobutton(
            self.reports_frame, text=questions[2], variable=self.report_name, value="report3")
        self.q3_button.pack(anchor="w")

        self.q4_button = Radiobutton(
            self.reports_frame, text=questions[3], variable=self.report_name, value="report4")
        self.q4_button.pack(anchor="w")

        self.button_frame = Frame(self)
        self.button_frame.pack(padx=5, pady=5)

        # Create and Close buttons
        self.create_button = Button(
            self.button_frame, text="Create", command=self.create, width=45)
        self.create_button.pack(padx=5, pady=5, side=LEFT)

        self.close_button = Button(
            self.button_frame, text="Close", command=self.close, width=10)
        self.close_button.pack(padx=5, pady=5)

    # This method is used when a manager clicks on the create button
    def create(self):
        while True:
            try:
                self.send_message(self.report_name.get())

                # Receive the report from the server and display it as a message box
                server_message = self.receive_message().split(";")
                if server_message[0] == "report1":
                    if len(server_message[1:]) > 1:
                        report_result = "The most popular coffees are "
                        for i in range(1, len(server_message[1:])+1):
                            if i > 1:
                                report_result += ", "
                            report_result += server_message[i]
                    elif len(server_message[1:]) == 1 and server_message[1] != "":
                        report_result = "The most popular coffee is " + \
                            server_message[1]
                    else:
                        report_result = "There is no coffee order."
                elif server_message[0] == "report2":
                    if len(server_message[1:]) > 1:
                        report_result = "The baristas with the highest number of orders are "
                        for i in range(1, len(server_message[1:])+1):
                            if i > 1:
                                report_result += ", "
                            report_result += server_message[i]
                    elif len(server_message[1:]) == 1 and server_message[1] != "":
                        report_result = "The barista with the highest number of orders is " + \
                            server_message[1]
                    else:
                        report_result = "There is no order taken by a barista."
                elif server_message[0] == "report3":
                    if len(server_message[1:]) > 1:
                        report_result = "The most popular products for the orders with the discount code are "
                        for i in range(1, len(server_message[1:])+1):
                            if i > 1:
                                report_result += ", "
                            report_result += server_message[i]
                    elif len(server_message[1:]) == 1 and server_message[1] != "":
                        report_result = "The most popular product for the orders with the discount code is " + \
                            server_message[1]
                    else:
                        report_result = "There is no order with the discount code."
                elif server_message[0] == "report4":
                    if len(server_message[1:]) > 1:
                        report_result = "The most popular cakes that are bought with expresso are "
                        for i in range(1, len(server_message[1:])+1):
                            if i > 1:
                                report_result += ", "
                            report_result += server_message[i]
                    elif len(server_message[1:]) == 1 and server_message[1] != "":
                        report_result = "The most popular cake that is bought with expresso is " + \
                            server_message[1]
                    elif len(server_message[1:]) == 1 and server_message[1] == "noexpressoorder":
                        report_result = "There is no expresso order in the system."
                    else:
                        report_result = "There is no cake that is bought with expresso."

                report_label = server_message[0][0].upper(
                ) + server_message[0][1:-1] + " " + server_message[0][-1]
                messagebox.showinfo(report_label, report_result)
                break

            # If the server is not available, display an error message and close the GUI
            except BlockingIOError or ConnectionAbortedError:
                messagebox.showerror(
                    "Connection Error", "The server is not available.")
                self.close()
                break

    # This method is used when a manager clicks on the close button
    def close(self):
        self.send_message("connectionclosed")
        self.master.destroy()
        self.client_socket.close()
        print("The client socket is closed.")

    # Method to send a message to the server
    def send_message(self, message):
        self.client_socket.send(message.encode())

    # Method to receive a message from the server
    def receive_message(self):
        return self.client_socket.recv(1024).decode()
