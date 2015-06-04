import os, sys

lib_path = os.path.abspath(os.path.join('.'))
sys.path.append(lib_path)

from english_list_parser import EnglishListParser

def test_language_string_with_ampersand():
    languages = EnglishListParser.parse_list("English & Spanish")

    assert languages == ["English", "Spanish"]

def test_language_string_with_commas():
    languages = EnglishListParser.parse_list("English, Spanish")

    assert languages == ["English", "Spanish"]

def test_language_string_with_and():
    languages = EnglishListParser.parse_list("English and Spanish")

    assert languages == ["English", "Spanish"]

def test_embedded_and():
    email_string = "justin.sanders@example.com and foo@example.com"
    emails = EnglishListParser.parse_list(email_string)

    assert emails == ["justin.sanders@example.com", "foo@example.com"]

def test_trailing_period():
    languages = EnglishListParser.parse_list("French, Spanish.")

    assert languages == ["French", "Spanish"]

def test_oxford_comma():
    language_string = "Tagalog, Farsi, and Chinese"
    languages = EnglishListParser.parse_list(language_string)

    assert languages == ["Tagalog", "Farsi", "Chinese"]

def test_or():
    emails = "foo@example.com, or bar@example.com or baz@example.com"
    email_list = EnglishListParser.parse_list(emails)

    assert email_list == ["foo@example.com", "bar@example.com", "baz@example.com"]

def test_ampersand():
    languages = EnglishListParser.parse_list("French, & Spanish")

    assert languages == ["French", "Spanish"]
