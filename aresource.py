#the class resource which has instance vars representing a resource in RCB


class Resource:
    def __init__(self,initinventory: int) -> None:
        self.inventory = initinventory
        self.state = initinventory
        self.waitlist = list()

    

    # add to wait list
    def processrequest(self,aresrceindex: int, reqamt: int) -> bool:
        #error checks 

        if self.state >= reqamt:
            self.state -= reqamt
            return True
            
        else:
            #add to wait list
            self.waitlist.append((aresrceindex,reqamt))

        return False

    def processrelease(self,releaseamt: int) -> [(int,int)]:
        self.state += releaseamt

        waitlist_iter = iter(self.waitlist)

        TheRetList = list()

        #check wait list for the list of process that can be process
        while len(self.waitlist) > 0 and self.state > 0:

            try:
                ThenextinWL = next(waitlist_iter)
            except StopIteration:
                break

            print(f"iterating over next: {ThenextinWL}")

            TheProcIndex = ThenextinWL[0]
            ThekAmt = ThenextinWL[1]

            print(f"the procind: {TheProcIndex}")

            if self.state >= ThekAmt:
                self.state -= ThekAmt

                #removing j,k from waitlist
                TheRetList.append(ThenextinWL)
            else:
                break

        #remove the items
        for atuple in TheRetList:
            self.waitlist.remove(atuple)

        return TheRetList





    def __repr__(self) -> str:
        return "Resource: " + "Inventory " + str(self.inventory) + " state " + str(self.state) + " waitlist " + str(self.waitlist)
        