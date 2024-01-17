import manager


def getfirsttwochar(astr):
    return astr[:2]



def mymain():
    # print("This is a test")

    Themanager = manager.Manager()

    FirstIn = True

    while(True):
        try:
            validcommand = 0

            userin = input()

            FirstArg = ""
            SecondArg = ""

            UserInarry = userin.split()

            for acount,anArg in enumerate(UserInarry):
                if acount == 1:
                    try:
                        FirstArg = int(anArg)
                    except:
                        FirstArg = ''
                elif acount == 2:
                    try:
                        SecondArg = int(anArg)
                    except:
                        SecondArg


            # try:
            #     FirstArg = int(userin.split(" ")[1])
            # except IndexError:
            #     FirstArg = ""

            # try:
            #     SecondArg = int(userin.split(" ")[2])
            # except IndexError:
            #     SecondArg = ""

            #need to check if arg are ints




            # print(f"echoing: '{userin} {FirstArg} {SecondArg}'")

            FirstTwoChar = getfirsttwochar(userin)

            try:

                if FirstTwoChar == "in":
                    # print("initialize")
                    Themanager.init()
                    # print(Themanager)
                    validcommand += 1

                elif FirstTwoChar == "cr":
                    # print("creating")

                    
                    Themanager.create(FirstArg)
                    validcommand += 1

                elif FirstTwoChar == "de":
                    # print("deleting")


                    Themanager.destroy(FirstArg)
                    validcommand += 1

                elif FirstTwoChar == "rq":
                    # print("requesting")


                    Themanager.request(FirstArg,SecondArg)
                    validcommand += 1

                elif FirstTwoChar == "rl":
                    # print("release")

                    Themanager.release(FirstArg,SecondArg)
                    validcommand += 1

                elif FirstTwoChar == "to":
                    # print("timeout")

                    Themanager.timeout()
                    validcommand += 1

                #printing
                    
                if validcommand > 0:

                    if FirstTwoChar == "in":
                        if FirstIn:
                            FirstIn = False
                            print(f"{Themanager.getcurrentProc()} ",end="")
                        else:
                            print(f"\n{Themanager.getcurrentProc()} ",end="")

                    else:
                        print(f"{Themanager.getcurrentProc()} ",end="")

                # print(Themanager)
                

                
            except Exception as e:
                # print(e)
                FirstIn = False
                print(f"-1 ",end='')
                

            




        except EOFError:
            # print("exiting")
            exit()
        except KeyboardInterrupt:
            exit()



if __name__ == "__main__":
    mymain()