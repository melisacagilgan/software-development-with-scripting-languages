""" This module contains the BaristaPanel class, which is the GUI for the barista. """

from tkinter import *
from tkinter import messagebox
from socket import *
from orders import create_order


class BaristaPanel(Frame):
    def __init__(self, barista, client_socket):
        self.barista = barista
        self.client_socket = client_socket

        # Create the GUI for the barista
        Frame.__init__(self)
        self.master.title('Barista Panel')
        self.pack()

        self.coffee_frame = Frame(self)
        self.coffee_frame.pack(padx=5, pady=5)
        self.coffee_label = Label(self.coffee_frame, text="COFFEES")
        self.coffee_label.pack(side="top")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)
        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)
        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)
        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5)

        self.cake_frame = Frame(self)
        self.cake_frame.pack(padx=5, pady=5)
        self.cake_label = Label(self.cake_frame, text="CAKES")
        self.cake_label.pack(side="top")

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5)
        self.frame6 = Frame(self)
        self.frame6.pack(padx=5, pady=5)
        self.frame7 = Frame(self)
        self.frame7.pack(padx=5, pady=5)

        self.coffee_frames = [self.frame1,
                              self.frame2, self.frame3, self.frame4]
        self.cake_frames = [self.frame5, self.frame6, self.frame7]

        # Create the entries for the coffees
        self.entry1 = Entry(self.frame1, state=DISABLED)
        self.entry2 = Entry(self.frame2, state=DISABLED)
        self.entry3 = Entry(self.frame3, state=DISABLED)
        self.entry4 = Entry(self.frame4, state=DISABLED)

        self.coffees = [("Latte", BooleanVar(), self.entry1), ("Cappuccino", BooleanVar(), self.entry2),
                        ("Americano", BooleanVar(), self.entry3), ("Expresso", BooleanVar(), self.entry4)]

        # Create the checkboxes for the coffees
        i = 0
        for frame in self.coffee_frames:
            self.cb = Checkbutton(
                frame, text=self.coffees[i][0], variable=self.coffees[i][1], command=self.activate_check_coffee)
            self.cb.pack(padx=5, pady=5, side=LEFT)
            self.coffees[i][2].pack(padx=5, pady=5)
            i += 1

        # Create the entries for the cakes
        self.entry5 = Entry(self.frame5, state=DISABLED)
        self.entry6 = Entry(self.frame6, state=DISABLED)
        self.entry7 = Entry(self.frame7, state=DISABLED)

        self.cakes = [("San Sebastian Cheesecake", BooleanVar(), self.entry5), ("Mosaic Cake", BooleanVar(), self.entry6),
                      ("Carrot Cake", BooleanVar(), self.entry7)]

        # Create the checkboxes for the cakes
        j = 0
        for frame in self.cake_frames:
            self.cb = Checkbutton(
                frame, text=self.cakes[j][0], variable=self.cakes[j][1], command=self.activate_check_cake)
            self.cb.pack(padx=5, pady=5, side=LEFT)
            self.cakes[j][2].pack(padx=5, pady=5)
            j += 1

        # Create the entry for the discount code
        self.frame8 = Frame(self)
        self.frame8.pack(padx=5, pady=5)
        self.discount_label = Label(self.frame8, text="Discount code, if any:")
        self.discount_label.pack(padx=5, pady=5, side=LEFT)
        self.discount = Entry(self.frame8)
        self.discount.pack(padx=5, pady=5)

        self.frame9 = Frame(self)
        self.frame9.pack(padx=5, pady=5)

        # Create and Close buttons
        self.create_button = Button(
            self.frame9, text="Create", command=self.create)
        self.create_button.pack(padx=5, pady=5, side=LEFT)

        self.close_button = Button(
            self.frame9, text="Close", command=self.close)
        self.close_button.pack(padx=5, pady=5)

    # This method is called when the barista ticks the checkbox of a cake
    def activate_check_cake(self):
        for i in range(len(self.cakes)):
            if self.cakes[i][1].get() == 1:
                self.cakes[i][2].config(state=NORMAL)
            elif self.cakes[i][1].get() == 0:
                self.cakes[i][2].delete(0, END)
                self.cakes[i][2].config(state=DISABLED)

    # This method is called when the barista ticks the checkbox of a coffee
    def activate_check_coffee(self):
        for i in range(len(self.coffees)):
            if self.coffees[i][1].get() == 1:
                self.coffees[i][2].config(state=NORMAL)
            elif self.coffees[i][1].get() == 0:
                self.coffees[i][2].delete(0, END)
                self.coffees[i][2].config(state=DISABLED)

    # This method is called when the barista clicks the create button
    def create(self):
        while True:
            try:
                # Create a product list with the products the barista has selected and their quantities
                # If the barista has not entered a quantity for a selected product, show an error message
                product_list = []
                for coffee in self.coffees:
                    if coffee[1].get() == 1 and coffee[2].get():
                        product_list.append(
                            (coffee[0].lower(), int(coffee[2].get())))
                    elif coffee[1].get() == 1 and not coffee[2].get():
                        messagebox.showerror(
                            "Error", "Please enter quantity for coffee")

                for cake in self.cakes:
                    if cake[1].get() == 1 and cake[2].get():
                        product_list.append(
                            (cake[0].lower().replace(" ", ""), int(cake[2].get())))
                    elif cake[1].get() == 1 and not cake[2].get():
                        messagebox.showerror(
                            "Error", "Please enter quantity for cake")

                # Create an order with the product list and the discount code the barista has entered
                order = create_order(self.discount.get(),
                                     self.barista, product_list)
                if len(order.split(";")[3:]) == 0:
                    messagebox.showinfo("Order Error", "Empty order")
                    break
                else:
                    self.send_message(order)
                    # If the server sends a confirmation message, show a message box with the total price
                    server_message = self.receive_message().split(";")
                    if server_message[0] == "orderconfirmation":
                        messagebox.showinfo(
                            "Total Price", "Total price is " + server_message[1])
                        self.clear_entries()
                    break

            # If the server is not running, show an error message and close the GUI
            except ConnectionRefusedError:
                messagebox.showerror("Connection Error",
                                     "The server is not running.")
                self.close()
                break

    # Clear the entries when the barista clicks the create button
    def clear_entries(self):
        for coffee in self.coffees:
            coffee[2].delete(0, END)
            coffee[2].config(state=DISABLED)
            coffee[1].set(0)

        for cake in self.cakes:
            cake[2].delete(0, END)
            cake[2].config(state=DISABLED)
            cake[1].set(0)

        self.discount.delete(0, END)

    # This method is called when the barista clicks the close button
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
