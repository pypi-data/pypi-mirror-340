from fc16004uno.no_lineal import biseccion
def test_biseccion():
    f = lambda x: x**3 - x - 2
    r = biseccion.biseccion(f, 1, 2)
    print("Bisección:", r)

if __name__ == "__main__":
    test_biseccion()