#the class process which has instance vars representing a process in PCB


class Process:
    def __init__(self,aparent: int, apriority: int):
        #0 ready 1 blocked running is implicit head of ready list at top one
        #which ever proc is at the begining of top most priority is running
        #even though the state may say 0 (ready)
        self.state = 0
        self.parent = aparent
        self.children = list()
        self.resource = [0] * 4
        self.priority = apriority

    def getparent(self):
        return self.parent
    
    def getchildren(self):
        return self.children

    def getpriority(self):
        return self.priority
    
    def getprocstate(self):
        return self.state
    
    def getresourcelist(self):
        return self.resource

    def setstate(self,agivstate:int):
        self.state = agivstate


    #need add and remove children
    def addchild(self,achild: int):
        self.children.append(achild)

    def removechild(self,achild: int):
        self.children.remove(achild)

    #need add and remove resources currently holding
    def addresource(self,resid: int,resamt: int):
        self.resource[resid] += resamt 

    def checkholdingresource(self,resid:int,relamt) -> bool:
        if self.resource[resid] >= relamt:
            return True
        return False

    def removeresource(self,resid: int,relamt: int):
        
        self.resource[resid] -= relamt 
        


    def setstate(self,astate:int):
        self.state = astate


    def __repr__(self) -> str:
        return "Process: state " + str(self.state) + " parent " + str(self.parent) + " children " + str(self.children) + " resource " + str(self.resource) + " priority " + str(self.priority)
        