from tkinter import *
import socket
from tkinter import messagebox

HOST = "127.0.0.1"
PORT = 5000
ADDR = (HOST, PORT)
SIZE = 1024
DISCONNECT_MSG = "!DISCONNECT"

class User(Frame):#Also called Login class but we prefer User.
    def __init__(self, client):
        Frame.__init__(self)
        self.client = client

        self.pack(expand=YES, fill=BOTH)
        self.master.title("LOGIN")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=20, pady=20)

        self.Label1 = Label(self.frame1, text="Username :")
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

        self.Login = Button(self.frame3, text="Login", command=self.LoginbuttonPressed)
        self.Login.pack(side=LEFT, padx=5, pady=5)

    #when login button pressed user credentials send to the server. If id and password is okay we get
    #users credential and make operation based on that.For example if barista is turned from server
    #Then barista window opens.
    def LoginbuttonPressed(self):
        username = self.userName.get()
        password = self.password.get()
        msg = "login;{};{}".format(username, password)
        # Send client user credential to the server
        self.client.send(msg.encode())
        # Read the response from the Server
        serverMsg = self.client.recv(SIZE).decode()
        print("[SERVER]" + serverMsg)
        operation = serverMsg.split(";")[0]

        if operation == "loginfailure":
            messagebox.showerror("Loginfailure", "Invalid Credentials")
            self.master.destroy()
        elif operation == "loginsuccess":
            userRole = serverMsg.split(";")[2]

            if userRole == "barista":
                self.master.destroy()
                newWindow = Barista(self.client, username)
            elif userRole == "manager":
                self.master.destroy()
                newWindow = Manager(self.client)
#Barista side.
class Barista(Frame):
    def __init__(self, client, baristaUserName):
        Frame.__init__(self)
        self.client = client
        self.baristaUserName = baristaUserName

        self.pack(expand = YES, fill = BOTH)
        self.master.title("Barista Panel")

        self.frame1 = Frame(self)
        self.frame1.pack()

        self.coffessLabel1 = Label(self.frame1, text = "COFFESS")
        self.coffessLabel1.pack(side = TOP)

        self.leftframeCoffess = Frame(self.frame1)
        self.leftframeCoffess.pack(side = LEFT)

        self.rightframeCoffess = Frame(self.frame1)
        self.rightframeCoffess.pack(side = RIGHT)

        self.coffess = [("Latte", BooleanVar()), ("Cappuccino", BooleanVar()), ("Americano", BooleanVar()),
                        ("Expresso", BooleanVar())]

        for coffess in self.coffess:
            self.coffessSelection = Checkbutton(self.leftframeCoffess, text = coffess[0], variable = coffess[1])
            self.coffessSelection.pack(fill = BOTH,pady = 2,padx = 45)

        self.latteAmount = Entry(self.rightframeCoffess, name="latte")
        self.latteAmount.pack(padx=45, pady=0)

        self.cappuccinoAmount = Entry(self.rightframeCoffess, name="cappuccino")
        self.cappuccinoAmount.pack(padx=45, pady=0)

        self.americanoAmount = Entry(self.rightframeCoffess, name="americano")
        self.americanoAmount.pack(padx=45, pady=0)

        self.expressoAmount = Entry(self.rightframeCoffess, name="expresso")
        self.expressoAmount.pack(padx=45, pady=0)

        self.frame2 = Frame(self)
        self.frame2.pack(side = TOP)

        self.cakesLabel1 = Label(self.frame2, text="CAKES")
        self.cakesLabel1.pack(side = TOP)

        self.leftframeCakes = Frame(self.frame2)
        self.leftframeCakes.pack(side = LEFT)

        self.rightframeCakes = Frame(self.frame2)
        self.rightframeCakes.pack(side = RIGHT)

        self.cakes = [("San Sebastian Cheesecake", BooleanVar()), ("Mosaic Cake", BooleanVar()),
                      ("Carrot Cake", BooleanVar())]

        for cakes in self.cakes:
            self.cakesSelection = Checkbutton(self.leftframeCakes, text = cakes[0], variable = cakes[1])
            self.cakesSelection.pack(fill = BOTH, pady = 2, padx = 0)

        self.sanSebatianAmount = Entry(self.rightframeCakes, name="sansebastianCheescake")
        self.sanSebatianAmount.pack(padx=45, pady=0)

        self.mosaicAmount = Entry(self.rightframeCakes, name="mosaiccake")
        self.mosaicAmount.pack(padx=45, pady=0)

        self.carrotcakeAmount = Entry(self.rightframeCakes, name="carrotcake")
        self.carrotcakeAmount.pack(padx=45, pady=0)

        self.leftframeCakes = Label(self.leftframeCakes, text = "Discount code,if any:")
        self.leftframeCakes.pack(fill = BOTH)
        self.enterDiscount = Entry(self.rightframeCakes, name = "discount")
        self.enterDiscount.pack(padx = 45, pady = 0)

        self.frame3 = Frame()
        self.frame3.pack(padx=5, pady=5)

        self.create = Button(self.frame3, text = "Create", command = self.createButton)
        self.create.pack(side=LEFT, padx=5, pady=5)
        self.close = Button(self.frame3, text = "Close", command = self.closeButton)
        self.close.pack(side=RIGHT, padx=5, pady=5)
    #wenever create button pressed order which is given by barista send to the server
    def createButton(self):
        coffessSelection = ""
        coffessAmount = ""
        cakesSelection = ""
        cakesAmount = ""
        discount = ""
        if self.enterDiscount.get():
            discount += self.enterDiscount.get()
        else:
            discount += "nodiscountcode"

        for coffess in self.coffess:
            if coffess[1].get():
                coffessSelection += ";" + coffess[0]
                if coffess[0] == "Latte":
                    coffessAmount += self.latteAmount.get()
                elif coffess[0] == "Cappuccino":
                    coffessAmount += self.cappuccinoAmount.get()
                elif coffess[0] == "Americano":
                    coffessAmount += self.americanoAmount.get()
                elif coffess[0] == "Expresso":
                    coffessAmount += self.expressoAmount.get()
                coffessSelection += "-" + coffessAmount
                coffessAmount = ""
            msgcoffee = "order;{};{}{}".format(discount,self.baristaUserName,coffessSelection)
        for cakes in self.cakes:
            if cakes[1].get():
                cakesSelection += ";" + cakes[0].replace(" ", "")
                cakesSelection = cakesSelection.replace("Cheesecake","")
                cakesSelection = cakesSelection.replace("Cake","")
                if cakes[0] == "San Sebastian Cheesecake":
                    cakesAmount += self.sanSebatianAmount.get()
                elif cakes[0] == "Mosaic Cake":
                    cakesAmount += self.mosaicAmount.get()
                elif cakes[0] == "Carrot Cake":
                    cakesAmount += self.carrotcakeAmount.get()
                cakesSelection += "-" + cakesAmount
                cakesAmount = ""
            msgcakes = "{}".format(cakesSelection)
        msg = msgcoffee + msgcakes
        self.client.send(msg.lower().encode())
        serverMsg = self.client.recv(SIZE).decode()
        print("[SERVER] " + serverMsg)
        serverMsg = serverMsg.split(";")
        messagebox.showinfo("Message", "Total Price:{}".format(serverMsg[1]))
    #disconnect
    def closeButton(self):
        msg = DISCONNECT_MSG
        self.client.send(msg.encode())
        self.master.destroy()
#Manager side
class Manager(Frame):
    def __init__(self,client):
        Frame.__init__(self)
        self.client = client

        self.pack(expand = YES, fill = BOTH)
        self.master.title("Manager Panel")

        self.frame1 = Frame(self)
        self.frame1.pack()

        self.Label1 = Label(self.frame1, text = "REPORTS")
        self.Label1.pack(side = TOP)

        self.frame2 = Frame(self)
        self.frame1.pack()

        self.chooseText = ["(1) What is the most popular coffee overall?",
                           "(2) Which barista has the highest number of orders?",
                           "(3) What is the most popular product for the orders with the discount code?",
                           "(4) What is the most popular cake that is bought with expresso?"]

        self.managerC = StringVar()
        self.managerC.set(self.chooseText[0])

        for choice in self.chooseText:
            self.optionSelect = Radiobutton(self.frame1, text=choice, value=choice, variable=self.managerC)
            self.optionSelect.pack(side=TOP, ipadx=10, ipady=10)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=10, pady=10)

        self.request = Button(self.frame2, text="Create", command=self.createButton)
        self.request.pack(side=LEFT, padx=5, pady=5)

        self.close = Button(self.frame2, text="Close", command=self.closeButton)
        self.close.pack(side=LEFT, padx=5, pady=5)

    #whenever manager press create button report will be send to the server and response taking back from the server.
    def createButton(self):
        opselect = self.managerC.get()
        # This if else chain's purpose is, read the response from the Server
        if opselect == "(1) What is the most popular coffee overall?":
            msg = "report1"
            self.client.send(msg.encode())

            serverMsg = self.client.recv(SIZE).decode()
            print("[SERVER] " + serverMsg)
            serverMsg = serverMsg.replace("report1;", "")
            messagebox.showinfo("Answer", "{}".format(serverMsg.upper()))

        elif opselect == "(2) Which barista has the highest number of orders?":
            msg = "report2"
            self.client.send(msg.encode())

            serverMsg = self.client.recv(SIZE).decode()
            print("[SERVER] " + serverMsg)
            serverMsg = serverMsg.replace("report2;", "")
            messagebox.showinfo("Answer", "{}".format(serverMsg.upper()))
        elif opselect == "(3) What is the most popular product for the orders with the discount code?":
            msg = "report3"
            self.client.send(msg.encode())

            serverMsg = self.client.recv(SIZE).decode()
            print("[SERVER] " + serverMsg)
            serverMsg = serverMsg.replace("report3;", "")
            messagebox.showinfo("Answer", "{}".format(serverMsg.upper()))
        elif opselect == "(4) What is the most popular cake that is bought with expresso?":
            msg = "report4"
            self.client.send(msg.encode())

            serverMsg = self.client.recv(SIZE).decode()
            print("[SERVER] " + serverMsg)
            serverMsg = serverMsg.replace("report4;", "")
            messagebox.showinfo("Answer", "{}".format(serverMsg.upper()))

    #disconnect
    def closeButton(self):
        msg = DISCONNECT_MSG
        self.client.send(msg.encode())
        self.master.destroy()


def main():
    # Create Socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Make connection request
        client.connect(ADDR)
    except socket.error:
        print("Call to connect failed")

    print(f"[CONNECTED] Client connected to server at {HOST}:{PORT}")
    serverMsg = client.recv(SIZE).decode()
    # To Check whether we get the connectionsuccess
    print(f"[SERVER] {serverMsg}")

    window1 = User(client)
    window1.mainloop()

if __name__ == "__main__":
    main()
