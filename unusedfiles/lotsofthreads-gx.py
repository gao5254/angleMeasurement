import time
import threading
import pyMT3 as mt

class NiceThread(threading.Thread):
    def __init__(self, portnum):
        super().__init__()
        (err, self.handle, self.ind) = mt.open_device(portnum)
        self.mylock = threading.Lock()
        self.reading = 0.0
        self.isrunning = False
        self.numofread = 0



    def run(self):
        while self.isrunning:
            (err, num, _) = mt.get_number(self.handle, self.ind)
            with self.mylock:
                self.reading = num
                self.numofread = self.numofread + 1

    def mystart(self):
        self.isrunning = True
        self.start()

    def mystop(self):
        self.isrunning = False
        mt.close_device(self.handle)
        print("close finished")


    def readnum(self):
        with self.mylock:
            num = self.reading
            times = self.numofread
        return (num, times)

if __name__ == "__main__":
    ports = [4,5,6]
    lasers = []
    for i in range(3):
        laser = NiceThread(ports[i])
        laser.mystart()
        lasers.append(laser)

    thistime = time.time()
    readings = [0, 0, 0]
    timesofreading = [0, 0, 0]
    for i in range(25):
        for j in range(3):
            (readings[j], timesofreading[j]) = lasers[j].readnum()
        print(readings + timesofreading)
        time.sleep(0.03)
    thattime = time.time()
    print(thattime - thistime)

    for i in range(3):
        lasers[i].mystop()
        lasers[i].join()
