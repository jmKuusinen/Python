'''Encoding ISO-8859-1'''
from pylibftdi import BitBangDevice

# USE THIS SCRIPT TO CONTROL CBUS-PINS ON FTDI-CHIPS W/ LINUX 
    

'''Possible I/O binary values'''
# 0x0F # [00001111] == all output

class FT232(BitBangDevice):

    def __init__(self, *o, **k) -> None:
        BitBangDevice.__init__(self, *o, **k)
        self.baudrate = 9600
        BitBangDevice.ftdi_fn.ftdi_set_line_property(5, 2, 0) # Set 5-bit data / 2 stop bits / no parity
        BitBangDevice.ftdi_fn.list_devices()

    # Set directions for available cbus-pins

    def iterate():
        print("Current pin status: ", BitBangDevice.ftdi_fn.read_pins())
        global directions
        directions = [0]
        i = 0
        cbusNumber = 0
        while i < 4:
            try:
                print("Specify direction for CBUS:", cbusNumber, "[0 / 1]")
                targetDir = int(input(">>>> \n"))
                if targetDir < 0 or targetDir > 1:
                    raise ValueError

                directions.append(targetDir)
                cbusNumber += 1
                i += 1


            except ValueError:
                print("Forbidden format! Enter [0 / 1]")

    # Translate into hex-format

    def Translate():
        str1 = "".join(str(x) for x in directions)
        print(str1) # Debug
        return hex(int(str1))
    # Set new state for each pin

    def switch(self):
        FT232.iterate()
        pinState = FT232.Translate()
        print(pinState, "Debug")
        with BitBangDevice('Serial') as bd: # Input device serial here

            bd.port |= pinState # Set pins high or low

    def close(self):
        BitBangDevice.ftdi_fn.close()






command = 'm'

while command != 'q':

    if command == 'a':
        dev = FT232()
        dev.switch()

    elif command == 'm':
        print("Commands: ", "m = Menu", "a = adjust CBUS", "q = Quit", sep= '\n')

    command = input('>>> ').strip().lower()

cleanDev = FT232()
cleanDev.close()