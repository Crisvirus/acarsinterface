
class IATAICAOConverter:
    def __init__(self,file):
        self.IATAtoICAO = {}
        csv_file = open(file, 'r')
        lines = csv_file.readlines()
        csv_file.close()
        for line in lines:
            tokens = line.split(',')
            if tokens[3] != '':
                self.IATAtoICAO[tokens[3].replace('"', '')] = (tokens[4].replace('"', ''),tokens[1].replace('"', ''))
                # print(tokens[1].replace('"', '') + " " +tokens[3].replace('"', '') + " "+tokens[4].replace('"', ''))

    def convert(self,flight_no):
        IATACode = flight_no[:-4]
        number = flight_no[-4:]
        try:
            number = int(number)
        except:
            print("Weird Number\n")
        if IATACode in self.IATAtoICAO:
            ICAOCode = self.IATAtoICAO[IATACode][0]
            if ICAOCode == '\\N':
                ICAOCode = IATACode
            ICAOFlight = ICAOCode + str(number)
            airline = self.IATAtoICAO[IATACode][1]
        else:
            ICAOFlight = "UNKNOWN"
            airline = "UNKNOWN"
        # print(ICAOFlight + " " + airline)
        return ICAOFlight,airline
            