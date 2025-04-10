from typing import List

class Tokenizer:

    """
    A Simple Tokenizer class used for creating tokens
    """

    def __init__(self,offset=0):
        self.offset = offset

    def encoder(self,text: str) -> List[int]:
        """
        Encode the given string

        :param
            text (str) : string to encode
        :returns
            List : list of tokens after encoding
        :raises
            ValueError : if Char in string is non-ASCII
        """

        for char in list(text):
            if ord(char) > 127:
                raise ValueError("Non ASCII Characters are not supported for Encoding")

        return [ ord(char)+self.offset for char in list(text) ]

    def decoder(self,tokens:List[int]) -> str :

        """
        :param
            tokens List[int]:
        :return:
            str : Decoded string
        :raises
            TypeError: If List contains any Non Integer Value
        """
        for num in tokens:
            if not isinstance(num,int):
                raise TypeError("The tokens generated must be of type int")

        return ''.join([chr(int(char) - self.offset) for char in list(tokens)])
