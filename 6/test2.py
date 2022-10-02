from app2 import Player, WordFactory

def test_create_word():
    factory = WordFactory({
        "h1",
        "buy",
        "hello",
        "affix",
        "afoot",
        "after",
        "again",
    })
    factory = factory.get_words_len(5)
    assert len(factory.get_words()) == 5


def test_guess_letter():
    factory = WordFactory({
        "h1",
        "buy",
        "hello",
        "affix",
        "afoot",
        "after",
        "again",
    })
    factory = factory.get_words_len(5)
    factory = factory.exclude_words_with_latter('a', 0)
    assert len(factory.get_words()) == 1
    assert "hello" in factory.get_words()


def test_guess_latter():
    p = Player({
        "h1",
        "buy",
        "hello",
        "affix",
        "afoot",
        "after",
        "again",
    }, 5)
    status = p.guess('a', 0)
    assert status == "MISS"

    # here only word hello
    for i, latter in enumerate("hello"):
        status = p.guess(latter, i)
        assert status == "OK"
