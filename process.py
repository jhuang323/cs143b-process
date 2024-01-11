#the class process which has instance vars representing a process in PCB


class Process:
    def __init__(self,aparent: int, apriority: int):
        #0 ready 1 running 2 blocked
        self.state = 0
        self.parent = aparent
        self.children = list()
        self.resource = [0] * 4
        self.priority = apriority

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

    def removeresource(self,resid: int,resamt: int):
        self.resource[resid] -= resamt 


    def setstate(self,astate:int):
        self.state = astate


    def __repr__(self) -> str:
        return "Process: state " + str(self.state) + " parent " + str(self.parent) + " children " + str(self.children) + " resource " + str(self.resource) + " priority " + str(self.priority)
        