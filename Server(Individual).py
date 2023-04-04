import socket, threading

HOST = "127.0.0.1"
PORT = 5000
ADDR = (HOST, PORT)
SIZE = 1024
DISCONNECT_MSG = "!DISCONNECT"
lock = threading.RLock()

#Check the users role, id and password situation
def userCredentialCheck(username, password):
    try:
        file = open("users.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            if username == lineArray[0] and password == lineArray[1]:
                username = lineArray[0]
                userRole = lineArray[2]
                file.close()
                return username, userRole, True
        username = ""
        userRole = ""
        file.close()
        return username, userRole, False

    except IOError:
        print("File could not be opened!")
        exit(1)
#read price file and return the total price.
def gettotalPrice(dict):
    try:
        totalPrice = 0
        file = open("prices.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            if dict[lineArray[0]] != 0:
                price = int(lineArray[1])
                dict[lineArray[0]] = dict[lineArray[0]] * int(price)
                totalPrice += dict[lineArray[0]]
        file.close()
        return totalPrice

    except IOError:
        print("File could not be opened!")
        exit(1)
#if discount code is used this function basically erase it.
def rewriteDiscount(count):
    try:
        lock.acquire()
        file = open("discountcodes.txt", "r")
        lines = file.readlines()
        file.close()

        file = open("discountcodes.txt", "w")
        for number,lines in enumerate(lines):
            if number != count-1:
                file.write(lines)
        file.close()
        lock.release()

    except IOError:
        print("File could not be opened!")
        exit(1)
#check if there is a discount code given or not
def checkDiscount(discountCode, totalPrice):
    try:
        count = 0
        file = open("discountcodes.txt", "r")
        for lines in file:
            count += 1
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            if lineArray[0] == discountCode:
                discountRate = lineArray[1]
                totalPrice = totalPrice - (int(lineArray[1])*totalPrice)/100
                break
        file.close()
        rewriteDiscount(count)
        return totalPrice, discountRate

    except IOError:
        print("File could not be opened!")
        exit(1)
#creates order.txt if it is not created and writes the order given by barista.
def orderText(msg):
    try:
        lock.acquire()
        file=open("orders.txt", "a")
        file.write("\n")
        file.write(msg)
        file.close()
        lock.release()

    except IOError:
        print("File could not be opened")
        exit(1)

#reading order from the file.
def readOrder(report):
    productdict = {"latte": 0, "cappuccino": 0, "americano": 0, "expresso": 0,
                   "sansebastian": 0, "mosaic": 0, "carrot": 0}#for report 3
    coffeedict = {"latte": 0, "cappuccino": 0, "americano": 0, "expresso": 0}#for report 1
    cakedict = {"sansebastian": 0, "mosaic": 0, "carrot": 0}#for report 4
    product = ""
    baristaCount1 = 0
    baristaCount2 = 0
    try:
        file = open("orders.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            lineArray.append("\0")
            if report == "report1":
                i = 3
                while lineArray[i] != "\0":
                    product = lineArray[i].split("-")
                    if product[0] in coffeedict:
                        coffeedict[product[0]] += int(product[1])
                    i += 1
                msg = [key for key, value in coffeedict.items() if value == max(coffeedict.values())]
                print(msg)
            if report == "report2":
                if lineArray[2] == "greg":
                    baristaCount1 += 1
                elif lineArray[2] == "dave":
                    baristaCount2 += 1
                if baristaCount1 > baristaCount2:
                    msg = ['greg']
                else:
                    msg = ['dave']
            if report == "report3":
                i = 3
                if lineArray[1] != "0":
                    while lineArray[i] != "\0":
                        product = lineArray[i].split("-")
                        if product[0] in productdict:
                            productdict[product[0]] += int(product[1])
                        i += 1
                msg = [key for key, value in productdict.items() if value == max(productdict.values())]
                print(msg)
            if report == "report4":
                i = 3
                if any("expresso" in word for word in lineArray):
                    while lineArray[i] != "\0":
                        product = lineArray[i].split("-")
                        if product[0] in cakedict:
                            cakedict[product[0]] += int(product[1])
                        i += 1
                    msg = [key for key, value in cakedict.items() if value == max(cakedict.values())]
                elif (cakedict["sansebastian"] == 0) and (cakedict["mosaic"] == 0) and (cakedict["carrot"] == 0):
                    msg = ['Couldnt Find Any']
        file.close()
        return msg
    except IOError:
        print("File could not be opened!")
        exit(1)

class ClientThread(threading.Thread):
    def __init__(self, clientSocket, clientAddress):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        print(f"[NEW CONNECTION] {clientAddress} connected.")
        msg = "connectionsuccess"
        self.clientSocket.send(msg.encode())

    def run(self):
        while True:
            msg = self.clientSocket.recv(SIZE).decode()
            print(f"[{self.clientAddress}] {msg}")
            clientMsg = msg.split(";")
            operation = clientMsg[0]
            if operation == DISCONNECT_MSG:
                break
            elif operation == "login":#Checking login and other requirements
                username = clientMsg[1]
                password = clientMsg[2]
                username, userRole, flag = userCredentialCheck(username, password)
                if flag:
                    serverMsg = "loginsuccess;{};{}".format(username, userRole)
                    self.clientSocket.send(serverMsg.encode())
                else:
                    serverMsg = "loginfailure"
                    print("SERVER sending login failure message")
                    self.clientSocket.send(serverMsg.encode())
                    self.clientSocket.close()
                    print("Client at {} disconnected...".format(self.clientAddress))
            elif operation == "order":
                i = 3
                discount = clientMsg[1]
                #dictionary is created for order. We are increment the elements inside dictionary based on order.
                productdict = {"latte": 0, "cappuccino": 0, "americano": 0, "expresso": 0,
                               "sansebastian": 0, "mosaic": 0, "carrot": 0}
                clientMsg.append("\0")
                productHolder = ""
                while clientMsg[i] != "\0":
                    product = clientMsg[i].split("-")
                    if product[0] in productdict:
                        productdict[product[0]] = int(product[1])
                        productHolder += ";" + product[0] + "-" + product[1]
                    i += 1
                totalPrice = gettotalPrice(productdict)
                discountRate = 0
                if discount != "nodiscountcode":
                    totalPrice, discountRate = checkDiscount(discount, totalPrice)

                msg_Text = "{};{};{}{}".format(totalPrice,discountRate,clientMsg[2],productHolder)
                orderText(msg_Text)

                serverMsg = "orderconfirmation;{}".format(totalPrice)
                self.clientSocket.send(serverMsg.encode())
            #reports are creating inside a readOrder.
            elif operation == "report1" or operation == "report2" or operation == "report3" or operation == "report4":
                Msg = readOrder(operation)
                Msg.append("\0")
                fixedMsg = ""
                i = 0
                while Msg[i] != "\0":
                    fixedMsg += Msg[i] + " "
                    i += 1
                serverMsg = "{};{}".format(operation,fixedMsg)
                self.clientSocket.send(serverMsg.encode())


        self.clientSocket.close()
        print("Client at {} disconnected...".format(self.clientAddress))






def main():
    print("[STARTING] Server is starting...")

    # create a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # bind the socket to address
        server.bind(ADDR)
    except socket.error:
        print("Call to bind failed!")

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    while True:
        # wait for connection request
        server.listen(1)
        # establish connection for request
        clientSocket, clientAddress = server.accept()
        thread = ClientThread(clientSocket, clientAddress)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
