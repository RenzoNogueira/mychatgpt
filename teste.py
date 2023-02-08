import argparse

def helloWorld():
    print("Hello World!")

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-n", "--name", help="name of the person", type=str)


## executa a função helloWorld() se o arquivo for executado diretamente
if __name__ == "__main__":
    args = parser.parse_args()
    if args.verbose:
        print("verbosity turned on")
    if args.name:
        print("Hello " + args.name)
    # helloWorld()