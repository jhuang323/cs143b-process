
def mymain():
    print("This is a test")

    while(True):
        try:
            userin = input()

            print(f"echoing: {userin}")
        except EOFError:
            print("exiting")
            exit()
        except KeyboardInterrupt:
            exit()



if __name__ == "__main__":
    mymain()