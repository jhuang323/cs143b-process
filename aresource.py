#the class resource which has instance vars representing a resource in RCB


class Resource:
    def __init__(self,initinventory: int) -> None:
        self.inventory = initinventory
        self.state = initinventory
        self.waitlist = list()

    # add to wait list
    def processrequest(self,aprocindex: int, reqamt: int) -> bool:
        #error checks 

        if self.state >= reqamt:
            self.state -= reqamt
            return True
            
        else:
            #add to wait list
            self.waitlist.append((aprocindex,reqamt))

    def processrelease(self,releaseamt: int):
        self.state += releaseamt


    def __repr__(self) -> str:
        return "Resource: " + "Inventory " + str(self.inventory) + " state " + str(self.state) + " waitlist " + str(self.waitlist)
        