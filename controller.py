import time
import easyhid

def itos(v):
    lsb = v & 0xFF
    msb = v >> 8
    return lsb, msb

class XArm():
    def __init__(self):
        # Stores an enumeration of all the connected USB HID devices
        en = easyhid.Enumeration()
        #print(en)

        # return a list of devices based on the search parameters
        devices = en.find(vid=0x483,pid=0x5750)  # vid=1155, )
        #print(devices)

        # print a description of the devices found
        #for dev in devices:
        #    print(dev.description())

        assert len(devices) > 0
        self.dev = devices[0]

        # open a device
        self.dev.open()
        print('Connected to xArm device')

    def __del__(self):
        print('Closing xArm device')
        self.dev.close()

    def move_to(self, id, pos, time=0):
        """
        CMD_SERVO_MOVE
        0x55 0x55 len 0x03 [time_lsb time_msb, id, pos_lsb pos_msb]
        Servo position is in the range [0, 1000]
        """
        pos = pos+1000
        t_lsb, t_msb = itos(time)
        p_lsb, p_msb = itos(pos)
        self.dev.write([0x55, 0x55, 8, 0x03, 1, t_lsb, t_msb, id, p_lsb, p_msb])

    def move_all(self, poss, time=0):
        """
        Set the position of all servos at once
        """

        for i in range(6):
            self.move_to(id=i + 1, pos=poss[i], time=time)

    def servos_off(self):
        self.dev.write([0x55, 0x55, 9, 20, 6, 1, 2, 3, 4, 5, 6])

    def rest(self):
        return self.arm.rest()

    def recieve_waste(self):
        # default position
        self.move_to(id=1, pos=500, time=1000)
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=-100, time=1000)
        self.move_to(id=4, pos=-100, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        time.sleep(2)

        # grab motion
        self.move_to(id=5, pos=1000, time=1000)
        time.sleep(1)
        self.move_to(id=1, pos=500, time=1000)
        time.sleep(1)
        self.move_to(id=1, pos=1200, time=1000)
        time.sleep(2)

        # default position with grab
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=500, time=1000)
        self.move_to(id=4, pos=500, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        
        # drop motion
        self.move_to(id=4, pos=1500, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        time.sleep(2)
        self.move_to(id=1, pos=500, time=1000)
        time.sleep(2)

        # default position
        self.move_to(id=1, pos=500, time=1000)
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=-100, time=1000)
        self.move_to(id=4, pos=-100, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        time.sleep(1)

    def recieve_recycle(self):

        # default position
        self.move_to(id=1, pos=500, time=1000)
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=-100, time=1000)
        self.move_to(id=4, pos=-100, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        time.sleep(2)

        # grab motion
        self.move_to(id=5, pos=1000, time=1000)
        time.sleep(1)
        self.move_to(id=1, pos=500, time=1000)
        time.sleep(1)
        self.move_to(id=1, pos=1200, time=1000)
        time.sleep(2)

        # default position with grab
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=500, time=1000)
        self.move_to(id=4, pos=500, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        
        # drop motion
        self.move_to(id=4, pos=1500, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=-100, time=1000)
        time.sleep(2)
        self.move_to(id=1, pos=500, time=1000)
        time.sleep(2)

        # default position
        self.move_to(id=1, pos=500, time=1000)
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=-100, time=1000)
        self.move_to(id=4, pos=-100, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        time.sleep(1)

    def recieve_compost(self):

        # default position
        self.move_to(id=1, pos=500, time=1000)
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=-100, time=1000)
        self.move_to(id=4, pos=-100, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        time.sleep(2)

        # grab motion
        self.move_to(id=5, pos=1000, time=1000)
        time.sleep(1)
        self.move_to(id=1, pos=500, time=1000)
        time.sleep(1)
        self.move_to(id=1, pos=1000, time=1000)
        time.sleep(2)

        # default position with grab
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=500, time=1000)
        self.move_to(id=4, pos=500, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        
        # drop motion
        self.move_to(id=4, pos=1500, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=500, time=1000)
        time.sleep(2)
        self.move_to(id=1, pos=500, time=1000)
        time.sleep(2)

        # default position
        self.move_to(id=1, pos=500, time=1000)
        self.move_to(id=2, pos=500, time=1000)
        self.move_to(id=3, pos=-100, time=1000)
        self.move_to(id=4, pos=-100, time=1000)
        self.move_to(id=5, pos=500, time=1000)
        self.move_to(id=6, pos=200, time=1000)
        time.sleep(1)

