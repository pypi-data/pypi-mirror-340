from hello_utils.greetings import say_hello

def test_say_hello():
    assert say_hello("World") == "Hello, World!"