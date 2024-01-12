import process
import manager


def main():
    print("in main function")

    aprocobj = process.Process(1,3)

    aprocobj.addchild(5)
    aprocobj.addchild(6)
    aprocobj.addchild(7)

    aprocobj.removechild(6)

    aprocobj.addresource(1,3)

    print(aprocobj)

    Themanager = manager.Manager()

    Themanager.init()
    print(Themanager)

    

    Themanager.create(1)
    Themanager.create(1)
    Themanager.create(1)
    Themanager.create(1)
    

    Themanager.request(2,2)

    # Themanager.create(1)
    # Themanager.create(2)

    # Themanager.request(0,1)

    # Themanager.timeout()

    # Themanager.request(1,1)

    # Themanager.request(0,1)

    # Themanager.request(1,1)



    Themanager.timeout()

    Themanager.request(2,1)

    Themanager.create(2)

    Themanager.request(2,1)
    # Themanager.request(2,1)

    Themanager.timeout()
    Themanager.timeout()

    # Themanager.request(2,1)

    #test release
    Themanager.release(2)

    

    

    

    print(Themanager)

    # Themanager.scheduler()


if __name__ == "__main__":
    main()