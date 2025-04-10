import pytest
from typing import List
from niktokenizer import Tokenizer

@pytest.fixture
def tokenizer():
    return Tokenizer(offset=5)

def test_encoder_valid_ascii(tokenizer):
    text = "Hello"
    expected = [ord(char) + 5 for char in text]
    assert tokenizer.encoder(text) == expected

def test_encoder_with_non_ascii_should_raise(tokenizer):
    text = "Héllo"  # 'é' is non-ASCII
    with pytest.raises(ValueError, match="Non ASCII Characters are not supported"):
        tokenizer.encoder(text)

def test_decoder_valid_tokens(tokenizer):
    original_text = "Test"
    tokens = [ord(char) + 5 for char in original_text]
    assert tokenizer.decoder(tokens) == original_text

def test_decoder_with_non_int_should_raise(tokenizer):
    invalid_tokens = [84, 101, "s", 116]  # 's' is not int
    with pytest.raises(TypeError, match="must be of type int"):
        tokenizer.decoder(invalid_tokens)

def test_round_trip_encoding_decoding(tokenizer):
    text = "Simple Test"
    encoded = tokenizer.encoder(text)
    decoded = tokenizer.decoder(encoded)
    assert decoded == text

def test_empty_string(tokenizer):
    assert tokenizer.encoder("") == []
    assert tokenizer.decoder([]) == ""