import socket
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime

# IP = socket.gethostbyname(socket.gethostname())
IP = "127.0.0.1"
PORT = 5000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


class Manager(Frame):
    def __init__(self, client):
        Frame.__init__(self)
        self.client = client

        self.pack(expand=YES, fill=BOTH)
        self.master.title("Manager")

        self.frame0 = Frame(self)
        self.frame0.pack(padx=20, pady=20)

        self.Label0 = Label(self.frame0, text="Select your report:")
        self.Label0.pack(side=TOP, padx=5, pady=5)

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.chooseText = ["(1) Which employee makes the highest number of reservations?",
                           "(2) Which apartment is the most popular?",
                           "(3) How many apartments are currently available?",
                           "(4) How many apartments have not been reserved yet?"]

        self.managerC = StringVar()
        self.managerC.set(self.chooseText[0])

        for choice in self.chooseText:
            self.optionSelect = ttk.Radiobutton(self.frame1, text=choice, value=choice, variable=self.managerC)
            self.optionSelect.pack(side=TOP, ipadx=10, ipady=10)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=10, pady=10)

        self.request = ttk.Button(self.frame2, text="Request", command=self.requestButtonPressed)
        self.request.pack(side=LEFT, padx=5, pady=5)

        self.close = ttk.Button(self.frame2, text="Close", command=self.closeButtonPressed)
        self.close.pack(side=LEFT, padx=5, pady=5)

    def requestButtonPressed(self):
        opselect = self.managerC.get()
        if opselect == "(1) Which employee makes the highest number of reservations?":
            msg = "report1"
            self.client.send(msg.encode(FORMAT))

            # Read the response from the Server
            serverMsg = self.client.recv(SIZE).decode(FORMAT)
            print("[SERVER] " + serverMsg)
            messagebox.showinfo("Information", "{} has the highest number of reservation".format(serverMsg))

        elif opselect == "(2) Which apartment is the most popular?":
            msg = "report2"
            self.client.send(msg.encode(FORMAT))

            # Read the response from the Server
            serverMsg = self.client.recv(SIZE).decode(FORMAT)
            print("[SERVER] " + serverMsg)
            messagebox.showinfo("Information", "{} is the most popular apartment".format(serverMsg))
        elif opselect == "(3) How many apartments are currently available?":
            msg = "report3"
            self.client.send(msg.encode(FORMAT))

            # Read the response from the Server
            serverMsg = self.client.recv(SIZE).decode(FORMAT)
            print("[SERVER] " + serverMsg)
            messagebox.showinfo("Information", "{} apartments are available now.".format(serverMsg))
        elif opselect == "(4) How many apartments have not been reserved yet?":
            msg = "report4"
            self.client.send(msg.encode(FORMAT))

            # Read the response from the Server
            serverMsg = self.client.recv(SIZE).decode(FORMAT)
            print("[SERVER] " + serverMsg)
            messagebox.showinfo("Information", "{} apartments have not been reserved yet.".format(serverMsg))

    def closeButtonPressed(self):
        msg = "terminate"
        self.client.send(msg.encode(FORMAT))
        self.master.destroy()


class Employee(Frame):
    def __init__(self, client, empUsername):
        Frame.__init__(self)
        self.client = client
        self.employeeUsername = empUsername

        self.pack(expand=YES, fill=BOTH)
        self.master.title("Employee")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=20, pady=20)

        self.Label1 = Label(self.frame1, text="Apartment Code:")
        self.Label1.pack(side=LEFT, padx=5, pady=5)

        self.apartmentCode = Entry(self.frame1, name="apartmentCode")
        self.apartmentCode.pack(side=RIGHT, padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=10, pady=10)

        self.Label2 = Label(self.frame2, text="Start Date:")
        self.Label2.pack(side=LEFT, padx=5, pady=5)

        self.startDate = Entry(self.frame2, name="startDate")
        self.startDate.pack(side=RIGHT, padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=10, pady=10)

        self.Label3 = Label(self.frame3, text="End Date:")
        self.Label3.pack(side=LEFT, padx=5, pady=5)

        self.endDate = Entry(self.frame3, name="endDate")
        self.endDate.pack(side=RIGHT, padx=5, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=10, pady=10)

        self.Label4 = Label(self.frame4, text="Customer Name:")
        self.Label4.pack(side=LEFT, padx=5, pady=5)

        self.customerName = Entry(self.frame4, name="customerName")
        self.customerName.pack(side=RIGHT, padx=5, pady=5)

        self.frame5 = Frame()
        self.frame5.pack(padx=10, pady=10)

        self.Show = ttk.Button(self.frame5, text="Show", command=self.ShowbuttonPressed)
        self.Show.pack(side=LEFT, padx=5, pady=5)

        self.frame6 = Frame()
        self.frame6.pack(padx=10, pady=10)

        self.Reserve = ttk.Button(self.frame6, text="Reserve", command=self.ReservebuttonPressed)
        self.Reserve.pack(side=LEFT, padx=5, pady=5)

    def ShowbuttonPressed(self):
        apartmentCode = self.apartmentCode.get()
        startDate = self.startDate.get()
        endDate = self.endDate.get()
        msg = "apartment;{};{};{}".format(apartmentCode, startDate, endDate)

        # Send client user credential to the server
        self.client.send(msg.encode(FORMAT))

        # Read the response from the Server
        serverMsg = self.client.recv(SIZE).decode(FORMAT)
        print("[SERVER] " + serverMsg)

        operation = serverMsg.split(";")[0]

        if operation == "invalidapartmentcode":
            messagebox.showerror("Error", "Invalid apartment code")
        else:
            availability = serverMsg.split(";")[6]
            if availability:
                address = serverMsg.split(";")[2]
                city = serverMsg.split(";")[3]
                postCode = serverMsg.split(";")[4]
                size = serverMsg.split(";")[5]
                noOfBedrooms = serverMsg.split(";")[6]
                screenMessage = "Apartment with {} code is available between {} and {}." \
                                " It's located at {} in {} with {} postcode. It has {} bedrooms and it's size is {} metersquare".format(
                    apartmentCode, startDate, endDate, address, city, postCode, noOfBedrooms, size)
                messagebox.showinfo("{}".format(apartmentCode), screenMessage)
            else:
                messagebox.showerror("Error",
                                     "Apartment ({}) is not available between {} and {} dates!".format(apartmentCode,
                                                                                                       startDate,
                                                                                                       endDate))

    def ReservebuttonPressed(self):
        apartmentCode = self.apartmentCode.get()
        startDate = self.startDate.get()
        endDate = self.endDate.get()
        customerName = self.customerName.get()
        msg = "reservation;{};{};{};{};{}".format(apartmentCode, customerName, startDate,
                                                  endDate, self.employeeUsername)

        # Send client user credential to the server
        self.client.send(msg.encode(FORMAT))

        # Read the response from the Server
        serverMsg = self.client.recv(SIZE).decode(FORMAT)
        print("[SERVER] " + serverMsg)
        print("Apartment code = {} , startDate= {} and endDate = {}".format(apartmentCode, startDate, endDate))
        if serverMsg == "successfulreservation":
            messagebox.showinfo("Reservation", "Reservation successfully added")
        elif serverMsg == "notavailable":
            messagebox.showerror("Error", "Apartment with ({}) code is not available between {} and {} dates".format(
                apartmentCode, startDate, endDate))
        elif serverMsg == "invalidapartmentcode":
            messagebox.showerror("Error", "Invalid apartment code")


class User(Frame):
    def __init__(self, client):
        Frame.__init__(self)
        self.client = client

        self.pack(expand=YES, fill=BOTH)
        self.master.title("LOGIN")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=20, pady=20)

        self.Label1 = Label(self.frame1, text="Username: ")
        self.Label1.pack(side=LEFT, padx=5, pady=5)

        self.userName = Entry(self.frame1, name="username")
        self.userName.pack(side=LEFT, padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=10, pady=10)

        self.Label2 = Label(self.frame2, text="Password: ")
        self.Label2.pack(side=LEFT, padx=5, pady=5)

        self.password = Entry(self.frame2, name="password", show="*")
        self.password.pack(side=LEFT, padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=10, pady=10)

        self.Login = ttk.Button(self.frame3, text="Login", command=self.LoginbuttonPressed)
        self.Login.pack(side=LEFT, padx=5, pady=5)

    def LoginbuttonPressed(self):
        username = self.userName.get()
        password = self.password.get()
        msg = "login;{};{}".format(username, password)
        # Send client user credential to the server
        self.client.send(msg.encode(FORMAT))
        # Read the response from the Server
        serverMsg = self.client.recv(SIZE).decode(FORMAT)
        print("[SERVER]" + serverMsg)
        operation = serverMsg.split(";")[0]

        if operation == "loginfailure":
            messagebox.showerror("Message", "Invalid Credentials")
            self.master.destroy()
        elif operation == "loginsuccess":
            userRole = serverMsg.split(";")[2]

            if userRole == "employee":
                self.master.destroy()
                newWindow = Employee(self.client, username)
            elif userRole == "manager":
                self.master.destroy()
                newWindow = Manager(self.client)


def main():
    # Create Socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Make connection request
        client.connect(ADDR)
    except socket.error:
        print("Call to connect failed")

    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    serverMsg = client.recv(SIZE).decode(FORMAT)
    # To Check whether we get the connectionsuccess
    print(f"[SERVER] {serverMsg}")

    window1 = User(client)
    window1.mainloop()


if __name__ == "__main__":
    main()
