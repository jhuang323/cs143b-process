import process
import aresource
# from queue import Queue


from collections import deque

#This is the process manager which is responsible for all proc

MAXPROCESSNUM = 16
#4 resources
MAXRESOURCENUM = 4

class Manager:
    def __init__(self) -> None:
        self.PCB = [None] * MAXPROCESSNUM
        self.RCB = [None] * MAXRESOURCENUM
        self.ReadyList2 = deque()
        self.ReadyList1 = deque()
        self.ReadyList0 = deque()
        #this is the state of the process that is selected to run implicit head of ready list
        self.currentprocessindex = 0

    
    def init(self):
        ''' The Init function for reseting the manager '''
        self.PCB = [None] * MAXPROCESSNUM
        self.RCB = [None] * MAXRESOURCENUM
        self.ReadyList2 = deque()
        self.ReadyList1 = deque()
        self.ReadyList0 = deque()

        #initialize PCB

        self.PCB[0] = process.Process(None,0)

        #initialize RCB

        self.RCB[0] = aresource.Resource(1)
        self.RCB[1] = aresource.Resource(1)
        self.RCB[2] = aresource.Resource(2)
        self.RCB[3] = aresource.Resource(3)

        #set current proc as 0
        self.currentprocessindex = 0

        # #set 0 as running
        # self.PCB[0].setstate(1)
        

        #add to ready list
        self.ReadyList0.append(0)

        # print("Init current process 0")

    def getcurrentProc(self):
        return self.currentprocessindex

    def scheduler(self):
        #returns the proc index that is scheduled to run
        #need to check all ready list to get highest process

        HighestProcessIndex = -1

        if len(self.ReadyList2) != 0:
            # print("readylist 2 not empty")
            HighestProcessIndex = self.ReadyList2[0]
        else:
            if len(self.ReadyList1) != 0:
                # print("readylist 1 not empty")
                HighestProcessIndex = self.ReadyList1[0]
            else:
                if len(self.ReadyList0) != 0:
                    # print("readylist 0 not empty")
                    HighestProcessIndex = self.ReadyList0[0] 

        # print(f"highest process: {HighestProcessIndex}" )

        #check if it is not the same
        if HighestProcessIndex != self.currentprocessindex:
            #perf context switch
            # print("perf context switch")

            

            self.currentprocessindex = HighestProcessIndex

        #return the highestind
            # print(f"highest priority ind: {HighestProcessIndex}")
        return HighestProcessIndex


    def create(self, priorval: int):

        #check it is 1 or 2
        if priorval > 2 or priorval < 1:
            raise "Error in Priority Value"

        #first find an empty spot in PCB if it exists
        try:
            firstEmptySpotindx = self.PCB.index(None)
        except ValueError:
            raise "Error max process reached"

        

        # print("empty spot" + str(firstEmptySpotindx))

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
                # print("error invalid proior")
                raise "Error in priority val"

        #call scheduler
        self.scheduler()


    def request(self,rind: int, kamt: int):
        '''request the resources'''

        #perform errorchecking on whether resource exceed capacity and current has

        #check if request if between 0-3
        if rind < 0 or rind > 3:
            raise "Error resource index out of bound"
        
        #check kamt
        if kamt < 0 or kamt > 3:
            raise "Error kamt is out of bounds"
        
        #check if proc 0 is requesting
        if self.currentprocessindex == 0:
            raise "Error proc 0 cannot req"

        


        #try to acquire
        CurprocIndex = self.currentprocessindex
        CurrentProc = self.PCB[CurprocIndex]

        #check request can be satisfy according to error check  numheld + request
        if CurrentProc.getresourcelist()[rind] + kamt > self.RCB[rind].getinventory():
            raise "Error req and hold exceed inventory"
        
        # print(f"is waitlist empty {self.RCB[rind].iswaitlistempty()}")

        if self.RCB[rind].processrequest(self.currentprocessindex,kamt) is True:
            CurrentProc.addresource(rind,kamt)
        else:
            #fail to acquire
            #state block
            CurrentProc.setstate(1)
            #remove from ready list
            tempCurProcRLInd = CurrentProc.getpriority()

            match tempCurProcRLInd:
                case 2:
                    self.ReadyList2.remove(CurprocIndex)
                case 1:
                    self.ReadyList1.remove(CurprocIndex)
                case 0:
                    self.ReadyList0.remove(CurprocIndex)

            # print(f"process {CurprocIndex} blocked")

            self.scheduler()


    def timeout(self):
        '''simulates hardware interrupt'''

        CurrentProcess = self.PCB[self.currentprocessindex]
        tempcurProcInd = CurrentProcess.getpriority()

        tempstorePopped = -10

        match tempcurProcInd:
                case 2:
                    tempstorePopped = self.ReadyList2.popleft()
                    self.ReadyList2.append(tempstorePopped)
                case 1:
                    tempstorePopped = self.ReadyList1.popleft()
                    self.ReadyList1.append(tempstorePopped)
                case 0:
                    tempstorePopped = self.ReadyList0.popleft()
                    self.ReadyList0.append(tempstorePopped)

        self.scheduler()

        # print("timeout")


    def release(self,rind: int,kamt: int):
        #error check if rind exist, if current proc actually hold resource

        #check if request if between 0-3
        if rind < 0 or rind > 3:
            raise "Error release resource index out of bound"
        
        #check kamt
        if kamt < 0 or kamt > 3:
            raise "Error kamt is out of bounds release"
        

        #check if 0 is release
        if self.currentprocessindex == 0:
            raise "Error proc 0 cannot rel"
        


        CurProcess = self.PCB[self.currentprocessindex]

        #error check releasing  > holding

        if kamt > CurProcess.getresourcelist()[rind]:
            raise "Error releasing greater than holding"

        #need to modify
        if CurProcess.checkholdingresource(rind,kamt) is not True:
            raise "Error cannot release not hold resource"
        
        CurProcess.removeresource(rind,kamt)

        ThetuplesReady = self.RCB[rind].processrelease(kamt)

        # print(f"the tups ready {ThetuplesReady}")

        #interate over the list
        for atupready in ThetuplesReady:
            temptarproc = self.PCB[atupready[0]]

            temptarproc.addresource(rind,atupready[1])

            #set state ready
            temptarproc.setstate(0)

            #insert into ready list
            tempProcPriority = temptarproc.getpriority()

            match tempProcPriority:
                case 2:
                    self.ReadyList2.append(atupready[0])
                case 1:
                    self.ReadyList1.append(atupready[0])
                case 0:
                    self.ReadyList0.append(atupready[0])
        
        #call scheduler at end
        self.scheduler()

    def _isChild(self,atarprocid: int) -> bool:
        '''checks if a proc index is a child of current'''

        Theproc = self.PCB[atarprocid]

        #check if theproc is none

        if Theproc is None:
            return False

        while Theproc.getparent() is not None:
            
            if Theproc.getparent() == self.currentprocessindex:
                return True
            
            Theproc = self.PCB[Theproc.getparent()]

        return False
    

    def _recurdestroy(self,aprocindx: int,finalindex:int):

        ThecurrentProc = self.PCB[aprocindx]

        ChildrenList = ThecurrentProc.getchildren()

        if len(ChildrenList) > 0:
            # print(f"child list {ChildrenList}")
            for achildindx in ChildrenList:
                # print(f"destroying {achildindx}")
                self._recurdestroy(achildindx,finalindex)
                # print(f"dest after {achildindx}")

        #destroy
                
        
        
        #remove from parent list
        Theparent = self.PCB[self.PCB[aprocindx].getparent()]

        if aprocindx == finalindex:

            Theparent.removechild(aprocindx)

        #remove from waiting or RL
        if ThecurrentProc.getprocstate() == 0:
            #remove from ready list

            tempProcPriority = ThecurrentProc.getpriority()

            #removing from ready list
            match tempProcPriority:
                case 2:
                    self.ReadyList2.remove(aprocindx)
                case 1:
                    self.ReadyList1.remove(aprocindx)
                case 0:
                    self.ReadyList0.remove(aprocindx)

        else:
            #remove from wait list 

            for aResourceObj in self.RCB:
                aResourceObj.removefromwaitinglist(aprocindx)

        #release all resource of j
        TheResourceList = ThecurrentProc.getresourcelist()

        for rind,kamt in enumerate(TheResourceList):
            # print(f"freeing {rind} {kamt}")

            CurProcess = ThecurrentProc

            #need to modify
            if CurProcess.checkholdingresource(rind,kamt) is not True:
                raise "Error cannot release not hold resource2"
            
            CurProcess.removeresource(rind,kamt)

            ThetuplesReady = self.RCB[rind].processrelease(kamt)

            # print(f"the tups ready {ThetuplesReady}")

            #interate over the list
            for atupready in ThetuplesReady:
                # print(f"atuuup {atupready}")
                temptarproc = self.PCB[atupready[0]]

                temptarproc.addresource(rind,atupready[1])

                #set state ready
                temptarproc.setstate(0)

                #insert into ready list
                tempProcPriority = temptarproc.getpriority()

                match tempProcPriority:
                    case 2:
                        self.ReadyList2.append(atupready[0])
                    case 1:
                        self.ReadyList1.append(atupready[0])
                    case 0:
                        self.ReadyList0.append(atupready[0])

        
        # print(f"finish destroy: {aprocindx}")
        #free pcb of J
        self.PCB[aprocindx] = None

        
        






    def destroy(self,aprocindx:int):
        '''destroy processes'''

        #check if out of bounds
        if aprocindx < 0 or aprocindx >= MAXPROCESSNUM:
            raise "Error Process index out of bounds"

        #check if 0
        if aprocindx == 0:
            raise "Error Proc 0 cannot be destroyed"

        #need to check if given proc index is child of currentprocess or equal
        if not self._isChild(aprocindx) and aprocindx != self.currentprocessindex:
            raise "Error proc is not it self or a child"

        #need to check if out of bounds


        self._recurdestroy(aprocindx,aprocindx)

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
    

    


        
        