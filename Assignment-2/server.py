import socket
import threading
from datetime import datetime, timedelta, date

# IP = socket.gethostbyname(socket.gethostname())
IP = "127.0.0.1"
PORT = 5000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
lock = threading.RLock()


def getApartmentInfo(apartmentCode):
    try:
        file = open("apartments.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            if apartmentCode == lineArray[0]:
                return lineArray[0], lineArray[1], lineArray[2], lineArray[3], lineArray[4], lineArray[5]
        file.close()
        return False
    except IOError:
        print("File could not be opened!")
        exit(1)


def checkApartmentCode(apartmentCode):
    try:
        file = open("apartments.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            if apartmentCode == lineArray[0]:
                file.close()
                return True
        file.close()
        return False
    except IOError:
        print("File could not be opened!")
        exit(1)


# Founded from https://www.codegrepper.com/code-examples/python/check+if+given+date+between+two+dates+python to compare the dates
def dateRange(startDate, endDate):
    # This function is appending the dates between start and end date in days list.
    delta = endDate - startDate  # as timedelta
    days = [startDate + timedelta(days=i) for i in range(delta.days + 1)]
    return days


def checkApartmentAvailability(apartmentCode, startDate, endDate):
    lock.acquire()
    found = False
    # Check that apartment is available or not
    apartmentFound = checkApartmentCode(apartmentCode)

    availability = False
    # If apartment is found in apartments.txt, we need to check whether the apartment is available between given times
    if apartmentFound:
        found = True
        apartmentFoundReservationsTxt = False
        try:
            file = open("reservations.txt", "r")
            for lines in file:
                lines = lines.replace("\n", "")
                lineArray = lines.split(";")
                # If Apartment Code is found in reservations.txt, we need to check time!
                if apartmentCode == lineArray[0]:
                    apartmentFoundReservationsTxt = True
                    sDateTxt = lineArray[2]
                    eDateTxt = lineArray[3]
                    # I convert string to datetime object in order to compare the times
                    startDateTxt = datetime.strptime(sDateTxt, "%d/%m/%Y")
                    endDateTxt = datetime.strptime(eDateTxt, "%d/%m/%Y")
                    days = dateRange(startDateTxt, endDateTxt)

                    if startDate and endDate not in days:
                        availability = True
                    else:
                        availability = False
                        apartmentCode = address = city = postCode = size = noOfBedroom = ""
                        lock.release()
                        return apartmentCode, address, city, postCode, size, noOfBedroom, availability, found

            file.close()
            # apartmentCode, address, city, postCode, size, noOfBedroom, availability, found
            if availability:
                apartmentCode, address, city, postCode, size, noOfBedroom = getApartmentInfo(apartmentCode)
                lock.release()
                return apartmentCode, address, city, postCode, size, noOfBedroom, availability, found

            if found and not apartmentFoundReservationsTxt:
                availability = True
                apartmentCode, address, city, postCode, size, noOfBedroom = getApartmentInfo(apartmentCode)
                lock.release()
                return apartmentCode, address, city, postCode, size, noOfBedroom, availability, found

        except IOError:
            print("File could not be opened!")
            exit(1)
    else:
        apartmentCode = address = city = postCode = size = noOfBedroom = ""
        lock.release()
        return apartmentCode, address, city, postCode, size, noOfBedroom, availability, found


def userCredentialCheck(username, password):
    try:
        lock.acquire()
        file = open("users.txt", "r")
        flag = False
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            if username == lineArray[0] and password == lineArray[1]:
                username = lineArray[0]
                userRole = lineArray[2]
                flag = True
                file.close()
                lock.release()
                return username, userRole, True
        username = ""
        userRole = ""
        lock.release()
        return username, userRole, False

    except IOError:
        print("File could not be opened!")
        exit(1)


def checkAvailable(apartmentCode, startDate, endDate):
    apartmentFound = checkApartmentCode(apartmentCode)
    apartmentFoundInReservationTxt = False
    availability = False
    try:
        file = open("reservations.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")

            # If Apartment Code is found in reservations.txt, we need to check time!
            if apartmentCode == lineArray[0]:
                apartmentFoundInReservationTxt = True
                sDateTxt = lineArray[2]
                eDateTxt = lineArray[3]

                # I converted the dates from string to datetime object
                sDate = datetime.strptime(startDate, "%d/%m/%Y")
                eDate = datetime.strptime(endDate, "%d/%m/%Y")

                # I convert string to datetime object in order to compare the times
                startDateTxt = datetime.strptime(sDateTxt, "%d/%m/%Y")
                endDateTxt = datetime.strptime(eDateTxt, "%d/%m/%Y")

                days = dateRange(startDateTxt, endDateTxt)
                if sDate and eDate not in days:
                    availability = True
                else:
                    return False

        if apartmentFound and not apartmentFoundInReservationTxt:
            return True

        if availability:
            return True

    except IOError:
        print("File could not be opened!")
        exit(1)


def writeReservation(line):
    lock.acquire()
    try:
        file = open("reservations.txt", "a")
        file.write("\n")
        file.write(line)
        file.close()

    except IOError:
        print("File could not be opened!")
        exit(1)
    lock.release()


def makeReservation(apartmentCode, customerName, startDate, endDate, employeeUsername):
    apartmentFound = checkApartmentCode(apartmentCode)
    if apartmentFound:
        available = checkAvailable(apartmentCode, startDate, endDate)
        if available:
            line = "{};{};{};{};{}".format(apartmentCode, customerName, startDate, endDate, employeeUsername)
            writeReservation(line)
            return "successfulreservation"
        else:
            return "notavailable"
    else:
        return "invalidapartmentcode"


def most_common(lst):
    return max(set(lst), key=lst.count)


def findWhichEmpHighestNoOfReservation():
    employeeList = []
    try:
        file = open("reservations.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            employee = lineArray[4]
            employeeList.append(employee)
    except IOError:
        print("File could not be opened!")
        exit(1)
    file.close()
    return most_common(employeeList)


def findMostPopularApartment():
    apartmentList = []
    try:
        file = open("reservations.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            apartment = lineArray[0]
            apartmentList.append(apartment)
    except IOError:
        print("File could not be opened!")
        exit(1)
    file.close()
    return most_common(apartmentList)


def getAllApartmentNames():
    apartmentList = []
    try:
        file = open("apartments.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            apartment = lineArray[0]
            apartmentList.append(apartment)
        file.close()
        return apartmentList
    except IOError:
        print("File could not be opened!")
        exit(1)


def findCurrentAvailableApartment():
    apartmentList = getAllApartmentNames()
    # today = "10/10/2015"
    today = date.today().strftime(
        "%d/%m/%Y")  # I get the date of today and convert it to string because checkAvailable function converts it to date object again and make its operations
    availableApartments = []
    for apartment in apartmentList:
        available = checkAvailable(apartment, today, today)
        if available:
            availableApartments.append(apartment)
    return availableApartments


def checkApartmentReservedOrNOt(apartmentName):
    try:
        file = open("reservations.txt", "r")
        for lines in file:
            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            if apartmentName == lineArray[0]:
                file.close()
                return False
        file.close()
        return True
    except IOError:
        print("File could not be opened!")
        exit(1)


def notReservedApartment():
    apartmentList = getAllApartmentNames()
    count = 0
    for apartment in apartmentList:
        found = checkApartmentReservedOrNOt(apartment)
        if found:
            count += 1
    return count


class ClientThread(threading.Thread):

    def __init__(self, clientSocket, clientAddress):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        print(f"[NEW CONNECTION] {clientAddress} connected.")
        msg = "connectionsuccess"
        self.clientSocket.send(msg.encode(FORMAT))

    def run(self):

        while True:
            msg = self.clientSocket.recv(SIZE).decode(FORMAT)
            print(f"[{self.clientAddress}] {msg}")
            clientMsg = msg.split(";")
            operation = clientMsg[0]

            if operation == "login":
                username = clientMsg[1]
                password = clientMsg[2]
                username, userRole, flag = userCredentialCheck(username, password)
                if flag:
                    msg = "loginsuccess;{};{}".format(username, userRole)
                    self.clientSocket.send(msg.encode(FORMAT))
                else:
                    msg = "loginfailure"
                    print("SERVER sending login failure message")
                    self.clientSocket.send(msg.encode(FORMAT))
            elif operation == "apartment":
                apartmentCode = clientMsg[1]
                sDate = clientMsg[2]
                eDate = clientMsg[3]
                startDate = datetime.strptime(sDate, "%d/%m/%Y")
                endDate = datetime.strptime(eDate, "%d/%m/%Y")

                apartmentCode, address, city, postCode, size, noOfBedroom, availability, found = checkApartmentAvailability(
                    apartmentCode, startDate, endDate)
                if not found:
                    msg = "invalidapartmentcode"
                    self.clientSocket.send(msg.encode(FORMAT))

                else:
                    msg = "apartment;{};{};{};{};{};{};{}".format(apartmentCode, address, city, postCode, size,
                                                                  noOfBedroom, availability)
                    self.clientSocket.send(msg.encode(FORMAT))
            elif operation == "reservation":
                apartmentCode = clientMsg[1]
                customerName = clientMsg[2]
                startDate = clientMsg[3]
                endDate = clientMsg[4]
                empUsername = clientMsg[5]
                msg = makeReservation(apartmentCode, customerName, startDate, endDate, empUsername)
                self.clientSocket.send(msg.encode(FORMAT))
            elif operation == "report1":
                empName = findWhichEmpHighestNoOfReservation()
                msg = "{}".format(empName)
                self.clientSocket.send(msg.encode(FORMAT))
            elif operation == "report2":
                aptName = findMostPopularApartment()
                msg = "{}".format(aptName)
                self.clientSocket.send(msg.encode(FORMAT))
            elif operation == "report3":
                availableApartment = findCurrentAvailableApartment()
                msg = "{}".format(len(availableApartment))
                self.clientSocket.send(msg.encode(FORMAT))
            elif operation == "report4":
                count = notReservedApartment()
                msg = "{}".format(count)
                self.clientSocket.send(msg.encode(FORMAT))
            elif operation == "terminate":
                break
        # self.clientSocket.send(bytes(msg, 'UTF-8'))
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

    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
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
