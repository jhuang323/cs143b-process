import process
import aresource
# from queue import Queue


from collections import deque

#This is the process manager which is responsible for all proc

MAXPROCESSNUM = 7

class Manager:
    def __init__(self) -> None:
        self.PCB = [None] * 5
        self.RCB = [None] * 4
        self.ReadyList2 = deque()
        self.ReadyList1 = deque()
        self.ReadyList0 = deque()
        self.currentprocessindex = 0

    
    def init(self):
        ''' The Init function for reseting the manager '''
        self.PCB[0] = process.Process(None,0)

        self.RCB[0] = aresource.Resource(1)
        self.RCB[1] = aresource.Resource(1)
        self.RCB[2] = aresource.Resource(2)
        self.RCB[3] = aresource.Resource(3)

        #set current proc as 0
        self.currentprocessindex = 0

        #set 0 as running
        self.PCB[0].setstate(1)
        

        #add to ready list
        self.ReadyList0.append(0)

        print("Init current process 0")

    def scheduler(self):
        #returns the proc index that is scheduled to run
        #need to check all ready list to get highest process

        HighestProcessIndex = -1

        if len(self.ReadyList2) != 0:
            print("readylist 2 not empty")
            HighestProcessIndex = self.ReadyList2[0]
        else:
            if len(self.ReadyList1) != 0:
                print("readylist 1 not empty")
                HighestProcessIndex = self.ReadyList1[0]
            else:
                if len(self.ReadyList0) != 0:
                    print("readylist 0 not empty")
                    HighestProcessIndex = self.ReadyList0[0] 

        print(f"highest process: {HighestProcessIndex}" )

        #check if it is not the same
        if HighestProcessIndex != self.currentprocessindex:
            #perf context switch
            print("perf context switch")

            #set to ready
            self.PCB[self.currentprocessindex].setstate(0)

            #change target to running
            self.PCB[HighestProcessIndex].setstate(1)

            self.currentprocessindex = HighestProcessIndex

        #return the highestind
            print(f"highest priority ind: {HighestProcessIndex}")
        return HighestProcessIndex


    def create(self, priorval: int):

        #first find an empty spot in PCB if it exists
        firstEmptySpotindx = self.PCB.index(None)

        if firstEmptySpotindx >= MAXPROCESSNUM:
            raise "Error max process reached"

        print("empty spot" + str(firstEmptySpotindx))

        #create process
        TheNewProc = process.Process(self.currentprocessindex,priorval)

        self.PCB[firstEmptySpotindx] = TheNewProc

        #update current process children
        self.PCB[self.currentprocessindex].addchild(firstEmptySpotindx)

        #enter into ready list

        match priorval:
            case 2:
                self.ReadyList2.append(firstEmptySpotindx)
            case 1:
                self.ReadyList1.append(firstEmptySpotindx)
            case 0:
                self.ReadyList0.append(firstEmptySpotindx)
            case _:
                print("error invalid proior")

        #call scheduler
        self.scheduler()




    def __repr__(self) -> str:
        theRetStr = f"Manager: {self.currentprocessindex} \nPCB\n"

        for anum,apcbobj in enumerate(self.PCB):
            theRetStr += str(anum) + str(apcbobj) + "\n"

        theRetStr += "\nRCB\n"

        for aind,arcbobj in enumerate(self.RCB):
            theRetStr += str(aind) + str(arcbobj) + "\n"

        theRetStr += "\nthe Ready list\n"
        
        

        theRetStr += "2 " + str(self.ReadyList2) + "\n"
        theRetStr += "1 " + str(self.ReadyList1) + "\n"
        theRetStr += "0 " + str(self.ReadyList0) + "\n"



        return theRetStr
    

    


        
        