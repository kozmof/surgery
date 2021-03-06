import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from surgery import surgery


global surgery_on
surgery_on = True


@surgery(surgery_on)
def test1(x, y, z):
    def test2(a):
        return 10 + a + x

    def test3():
        return 100

    def test4():
        a = 1000
        return a + z

    def test5(a, b, c, d):
        return a + b + c + d

    return x + y + z


class Test(unittest.TestCase):
    def test_return(self):
        if surgery_on:
            print("surgery is active")
            inner_f = test1(50, 100, 200)
            self.assertEqual(inner_f['test2'](100), 160)
            self.assertEqual(inner_f['test3'](), 100)
            self.assertEqual(inner_f['test4'](), 1200)
            self.assertEqual(inner_f['test5'](1, 2, 3, 4), 10)
        else:
            print("surgery is inactive")
            self.assertEqual(test1(50, 100, 200), 350)
    
if __name__ == "__main__":
    unittest.main()
