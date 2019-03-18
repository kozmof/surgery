surgery
-------

![alt image](https://img.shields.io/badge/version-0.1.0-blue.svg) ![alt image](https://img.shields.io/badge/Python-3.5-blue.svg)

A decorator for testing functions which are defined in a function. When you need to snap off surgery, pass False.

### Usage

```Python
@surgery(True)
def main(x, y, z):
    def test1(a):
        print(10 + a + x)

    def test2():
        print(100)

    def test3():
        print(z)

    def test4(a, b, c, d):
        print(a, b, c, d)

    def test5():
        return 150
        
if __name__ == "__main__":
    inner_f = main(50, 100, 200)
    inner_f['test1'](100) # 160
    inner_f['test2']() # 100
    inner_f['test3']() # 200
    inner_f['test4'](1, 2, 3, 4) # 1 2 3 4
    print(inner_f['test5']()) # 150
```

### Limitation
In an inner function, using a value defined in an outer function is not available.
