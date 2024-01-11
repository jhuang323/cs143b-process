import process


def main():
    print("in main function")

    aprocobj = process.Process(1,3)

    aprocobj.addchild(5)
    aprocobj.addchild(6)
    aprocobj.addchild(7)

    aprocobj.removechild(6)

    aprocobj.addresource(1,3)

    print(aprocobj)


if __name__ == "__main__":
    main()