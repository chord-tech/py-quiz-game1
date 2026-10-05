"""Question bank. Each entry: (level, question, correct answer, wrong1, wrong2).
Letters (a/b/c) are assigned and shuffled per attempt in app.py."""

_RAW = [
    # ---- easy (original 10 + 2) ----
    ("easy", "What is the output of the following code: print(2 + 3 * 4)?", "14", "20", "24"),
    ("easy", "What keyword is used to create a function in Python?", "def", "function", "create"),
    ("easy", "Which of the following is a mutable data type in Python?", "list", "tuple", "string"),
    ("easy", "What is the output of the following code: print(type([]))?", "<class 'list'>", "<class 'tuple'>", "<class 'dict'>"),
    ("easy", "What is the output of the following code: print(10 // 3)?", "3", "3.3333", "4"),
    ("easy", "Which function is used to display text or output on the screen?", "print()", "input()", "len()"),
    ("easy", "Which loop is commonly used to iterate through a sequence?", "for", "while", "do-while"),
    ("easy", "Which function is used to get input from a user?", "input()", "print()", "len()"),
    ("easy", "What is the output of the following code: print(len('Hello, World!'))?", "13", "12", "14"),
    ("easy", "Which data structure stores an ordered collection of items that can be changed?", "list", "tuple", "string"),
    ("easy", "Which symbol starts a single-line comment in Python?", "#", "//", "--"),
    ("easy", "Which operator checks whether two values are equal?", "==", "=", "!="),
    # ---- medium ----
    ("medium", "What is the output of print(type(3 / 2))?", "<class 'float'>", "<class 'int'>", "<class 'str'>"),
    ("medium", "What does my_list.append(x) do?", "Adds x to the end of the list", "Adds x to the start of the list", "Returns a new list with x added"),
    ("medium", "What is the output of print('ab' * 3)?", "ababab", "ab3", "It raises an error"),
    ("medium", "Which of these creates a dictionary?", "{'a': 1}", "['a', 1]", "{'a', 1}"),
    ("medium", "What is the output of print(bool([]))?", "False", "True", "None"),
    ("medium", "What does range(3) produce?", "0, 1, 2", "1, 2, 3", "0, 1, 2, 3"),
    ("medium", "If s = 'python', what is s[1:3]?", "'yt'", "'yth'", "'py'"),
    ("medium", "What is the output of print(7 % 3)?", "1", "2", "0"),
    ("medium", "What is the output of print('hello'.replace('l', 'L', 1))?", "heLlo", "heLLo", "Hello"),
    ("medium", "Which pair of keywords handles exceptions in Python?", "try / except", "try / catch", "handle / error"),
    ("medium", "What is the output of print('5' + '5')?", "55", "10", "It raises an error"),
    ("medium", "Which of these data types is immutable?", "tuple", "list", "dict"),
    # ---- hard ----
    ("hard", "def f(x, l=[]):\n  l.append(x)\n  return l\nf(1)\nWhat does print(f(2)) output?", "[1, 2]", "[2]", "[1]"),
    ("hard", "What is the output of print(list(range(10, 0, -3)))?", "[10, 7, 4, 1]", "[10, 7, 4]", "[10, 7, 4, 1, 0]"),
    ("hard", "What is the output of print(type(lambda: 0))?", "<class 'function'>", "<class 'lambda'>", "<class 'NoneType'>"),
    ("hard", "a = [1, 2, 3]; b = a; b.append(4). What is print(a)?", "[1, 2, 3, 4]", "[1, 2, 3]", "It raises an error"),
    ("hard", "What is the output of print(len({1, 2, 2, 3}))?", "3", "4", "2"),
    ("hard", "What is the output of print(any([0, '', None]))?", "False", "True", "None"),
    ("hard", "x = 10; def f(): x = 5; then f() is called. What does print(x) show?", "10", "5", "It raises an error"),
    ("hard", "What is the output of print([i * i for i in range(4)])?", "[0, 1, 4, 9]", "[1, 4, 9, 16]", "[0, 1, 4]"),
    ("hard", "What does the 'is' operator compare?", "Object identity", "Value equality", "Type only"),
    ("hard", "What is the output of print(round(2.5))?", "2", "3", "2.5"),
    ("hard", "For d = {'a': 1}, what does print(d.get('b', 0)) output?", "0", "None", "It raises a KeyError"),
    ("hard", "What is the output of print(bool('False'))?", "True", "False", "It raises an error"),
]

BANK = [
    {"id": i, "level": lvl, "question": q, "correct": c, "wrong": [w1, w2]}
    for i, (lvl, q, c, w1, w2) in enumerate(_RAW, start=1)
]
LEVELS = ("easy", "medium", "hard", "mixed")
QUIZ_SIZE = 10
MIXED_SPLIT = {"easy": 4, "medium": 3, "hard": 3}
