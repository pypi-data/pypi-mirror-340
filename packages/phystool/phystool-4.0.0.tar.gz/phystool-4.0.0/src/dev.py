from phystool.helper import greptex


def run_A() -> None:
    for f in greptex("ress", "/home/jdufour/travail/teaching/src-phys/physdb", silent=False):
        print(f)



if __name__ == "__main__":
    run_A()
