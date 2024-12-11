from aoc_plumber import It

def test_it_bool():
    assert list(filter(It < 5, range(10))) == [0, 1, 2, 3, 4]
    assert list(filter(It > 5, range(10))) == [6, 7, 8, 9]
    assert list(filter(It <= 5, range(10))) == [0, 1, 2, 3, 4, 5]
    assert list(filter(It >= 5, range(10))) == [5, 6, 7, 8, 9]
    assert list(filter(It == 5, range(10))) == [5]
    assert list(filter(It != 5, range(10))) == [0, 1, 2, 3, 4, 6, 7, 8, 9]

def test_it_compose():
    plus_1 = It + 1
    times_2 = It * 2
    assert list(map(plus_1 @ times_2, range(3))) == [1, 3, 5]

def test_it_numeric():
    assert list(filter(It % 2 == 0, range(10))) == [0, 2, 4, 6, 8]
    assert list(filter(It // 2 == 2, range(10))) == [4, 5]

def test_it_weird():
    assert list(map((It + 1) - It, range(10))) == [1] * 10
