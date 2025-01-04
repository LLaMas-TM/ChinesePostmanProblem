import unittest
from chinese_postman import ChinesePostman

class TestChinesePostman(unittest.TestCase):
    def test_simple_graph(self):
        cpp = ChinesePostman()
        cpp.add_node(1, 2, 4)
        cpp.add_node(1, 3, 3)
        cpp.add_node(1, 5, 10)
        cpp.add_node(2, 3, 2)
        cpp.add_node(2, 4, 3)
        cpp.add_node(3, 4, 3)
        cpp.add_node(4, 5, 9)

        total_cost, path = cpp.solve()
        self.assertEqual(total_cost, 40)
        self.assertEqual(path, [1, 2, 3, 1, 5, 4, 2, 4, 3, 1])

    def test_letter_nodes(self):
        cpp = ChinesePostman()
        cpp.add_node("A", "B", 3)
        cpp.add_node("B", "C", 4)
        cpp.add_node("C", "D", 5)
        cpp.add_node("D", "A", 2)
        cpp.add_node("A", "C", 1)

        total_cost, path = cpp.solve()
        self.assertEqual(total_cost, 16)
        self.assertEqual(path, ["A", "B", "C", "D", "A", "C", "A"])

    def test_complex_graph(self):
        cpp = ChinesePostman()
        cpp.add_node(1, 2, 8)
        cpp.add_node(1, 5, 4)
        cpp.add_node(1, 8, 3)
        cpp.add_node(2, 3, 9)
        cpp.add_node(2, 7, 6)
        cpp.add_node(3, 4, 5)
        cpp.add_node(3, 6, 3)
        cpp.add_node(4, 5, 5)
        cpp.add_node(4, 6, 1)
        cpp.add_node(5, 6, 2)
        cpp.add_node(5, 7, 3)
        cpp.add_node(7, 8, 1)

        total_cost, path = cpp.solve()
        self.assertEqual(total_cost, 64)
        self.assertEqual(path, [1, 2, 3, 4, 5, 1, 8, 7, 2, 3, 6, 4, 6, 5, 7, 8, 1])

    def test_cities(self):
        cpp = ChinesePostman()
        cpp.add_node("Warszawa", "Kraków", 293)
        cpp.add_node("Warszawa", "Gdańsk", 339)
        cpp.add_node("Warszawa", "Wrocław", 342)
        cpp.add_node("Warszawa", "Katowice", 320)
        cpp.add_node("Warszawa", "Poznań", 310)
        cpp.add_node("Gdańsk", "Poznań", 318)
        cpp.add_node("Wrocław", "Poznań", 164)
        cpp.add_node("Wrocław", "Katowice", 200)
        cpp.add_node("Poznań", "Szczecin", 272)
        cpp.add_node("Katowice", "Kraków", 76)

        total_cost, path = cpp.solve()
        self.assertEqual(total_cost, 3390)
        self.assertEqual(path, [
            "Warszawa", "Kraków", "Katowice", "Warszawa", "Gdańsk",
            "Poznań", "Warszawa", "Wrocław", "Poznań", "Szczecin",
            "Poznań", "Wrocław", "Katowice", "Warszawa"
        ])

if __name__ == '__main__':
    unittest.main()
