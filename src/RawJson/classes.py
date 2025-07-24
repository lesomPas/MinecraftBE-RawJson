from abc import ABC, abstractmethod
from .utils import is_single_string_value, is_single_dictionary_value, is_string_value
from pprint import pformat
from typing import Union, List, Dict, Any

class RawComponent(ABC):
    """Base class for all raw component types."""
    def with_id(self) -> str:
        """Return a unique identifier for the component."""
        return f"{id(self)}::{str(self)}"

    @abstractmethod
    def toDictionary(self) -> dict:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Rawtext(RawComponent):
    """Class for handling raw text components."""
    process = None  # Placeholder for processing function

    def __init__(self, dictionary: dict = {}) -> None:
        self.data = Rawtext.process(dictionary) if dictionary != {} else [] # if self.process else dictionary

    def toDictionary(self) -> dict:
        return {
            "rawtext": [i.toDictionary() for i in self.data]
        }

    def add(self, *args) -> 'Rawtext':
        for obj in args:
            if not isinstance(obj, RawComponent):
                raise TypeError("arguments must be rawcomponent")
            self.data.append(obj)
        return self

    def addAll(self, sequence: list[RawComponent]) -> 'Rawtext':
        return self.add(*sequence)

    def translate(self, translate: str) -> 'TranslateBuilder':
        if not isinstance(translate, str):
            raise TypeError("build failed")

        return TranslateBuilder(self, translate)

    def __str__(self) -> str:
        return pformat(self.data)

    def __repr__(self) -> str:
        return f"-rawtext::{str(self)}"


class TranslateBuilder(object):
    def __init__(self, raw: Rawtext, translate: str) -> None:
        if not isinstance(raw, Rawtext) or not isinstance(translate, str):
            raise TypeError("build failed")

        self.raw = raw
        self.translate = translate

    def build(self, *args) -> Rawtext:
        if args == []:
            return self.raw.add(Translate(self.translate))

        if any(not isinstance(i, RawComponent) for i in args):
            raise ValueError("build failed")

        withraw = Rawtext().addAll(args)
        return self.raw.add(Translate(self.translate, withraw))

    def strBuild(self, *args) -> Rawtext:
        if args == []:
            return self.raw.add(Translate(self.translate))

        if any(not isinstance(i, str) for i in args):
            raise ValueError("build failed")

        return self.raw.add(Translate(self.translate, args))

    def sequenceBuild(self, sequence: list[RawComponent]) -> Rawtext:
        return self.build(*sequence)

    def sequenceStrBuild(self, sequence: list[str]) -> Rawtext:
        return self.strBuild(*sequence)


class Text(RawComponent):
    def __init__(self, content: str) -> None:
        if not isinstance(content, str):
            raise TypeError("Content must be a string")
        self.content = content

    @staticmethod
    def toText(dictionary: dict) -> 'Text':
        if not is_single_string_value(dictionary, "text"):
            raise ValueError("Invalid dictionary: must contain single 'text' string value")
        return Text(dictionary["text"])

    @staticmethod
    def contentToDictionary(content: str) -> dict:
        if not isinstance(content, str):
            raise TypeError("Content must be a string")
        return Text.__toDictionary(content)

    @staticmethod
    def __toDictionary(content: str) -> dict:
        return {
            "text": content
        }

    def toDictionary(self) -> dict:
        return self.__toDictionary(self.content)

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return f"-text::{str(self)}"


class Score(RawComponent):
    def __init__(self, name: str, objective: str) -> None:
        if not (isinstance(name, str) and isinstance(objective, str)):
            raise TypeError("Name and Objective must be a string")

        self.name = name
        self.objective = objective

    @staticmethod
    def toScore(dictionary: dict) -> 'Score':
        if not is_single_dictionary_value(dictionary, "score"):
            raise ValueError("Invalid dictionary: must contain single 'score' dictionary value")

        data = dictionary["score"]
        if not is_string_value(data, ["name", "objective"]):
            raise ValueError("Score dictionary must contain 'name' and 'objective' string values")
        return Score(data["name"], data["objective"])

    @staticmethod
    def contentToDictionary(name: str, objective: str) -> dict:
        if not (isinstance(name, str) and isinstance(objective, str)):
            raise TypeError("Name and Objective must be a string")
        return Score.__toDictionary(name, objective)

    @staticmethod
    def __toDictionary(name, objective) -> dict:
        return {
            "score": {
                "name": name,
                "objective": objective
            }
        }

    def toDictionary(self) -> dict:
        return self.__toDictionary(self.name, self.objective)

    def __str__(self) -> str:
        return f"{self.name} >> {self.objective}"

    def __repr__(self) -> str:
        return f"-score::{str(self)}"


class Selector(RawComponent):
    def __init__(self, content: str) -> None:
        if not isinstance(content, str):
            raise TypeError("Content must be a string")
        self.content = content

    @staticmethod
    def toSelector(dictionary: dict) -> 'Selector':
        if not is_single_string_value(dictionary, "selector"):
            raise ValueError("Invalid dictionary: must contain single 'selector' string value")
        return Selector(dictionary["selector"])

    @staticmethod
    def contentToDictionary(content: str) -> dict:
        if not isinstance(content, str):
            raise TypeError("Content must be a string")
        return Selector.__toDictionary(content)

    @staticmethod
    def __toDictionary(content: str) -> dict:
        return {
            "selector": content
        }

    def toDictionary(self) -> dict:
        return self.__toDictionary(self.content)

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return f"-selector::{str(self)}"


class Translate(RawComponent):
    def __init__(self, translate: str, with_content: Union[List[str], Rawtext, None] = None) -> None:
        if with_content is not None:
            if not (isinstance(with_content, (list, Rawtext))):
                raise TypeError("'with' must be list of strings or Rawtext")
            
            if isinstance(with_content, list) and not all(isinstance(i, str) for i in with_content):
                raise TypeError("All items in 'with' list must be strings")

        self.translate = translate
        self.with_content = with_content

    @staticmethod
    def toTranslate(dictionary: dict) -> 'Translate':
        if "translate" not in dictionary:
            raise ValueError("Dictionary must contain 'translate' key")

        if not isinstance(dictionary["translate"], str):
            raise ValueError("'translate' value must be a string")

        with_content: Union[List[str], dict, None] = None

        if "with" not in dictionary:
            if len(dictionary) > 1:
                raise ValueError("Dictionary contains extra keys")
            return Translate(dictionary["translate"])

        if len(dictionary) > 2:
            raise ValueError("Dictionary contains extra keys")

        with_value = dictionary["with"]
        if isinstance(with_value, list) and all(isinstance(i, str) for i in with_value):
            return Translate(dictionary["translate"], with_value)
        elif isinstance(with_value, dict):
            return Translate(dictionary["translate"], Rawtext(with_value))
        else:
            raise ValueError("'with' must be a list of strings or a dictionary")

    @staticmethod
    def contentToDictionary(translate: str, with_content: Union[List[str], Rawtext, None]) -> dict:
        if not isinstance(translate, str):
            raise TypeError("'Translate' must be a string")

        if with_content is not None or not isinstance(with_content, Rawtext) or any(not isinstance(i, str) for i in with_content):
            raise TypeError("'With' error")

        return Translate.__toDictionary(translate, with_content)

    @staticmethod
    def __toDictionary(translate: str, with_content: Union[List[str], Rawtext, None]) -> dict:
        if with_content is None:
            return {
                "translate": translate
            }
        else:
            data = with_content.toDictionary() if isinstance(with_content, Rawtext) else with_content
            return {
                "translate": translate,
                "with": data
            }

    def toDictionary(self) -> dict:
        return self.__toDictionary(self.translate, self.with_content)

    def __str__(self) -> str:
        if self.with_content is not None:
            return f"{self.translate}\n  {pformat(self.with_content)}"
        return self.translate

    def __repr__(self) -> str:
        if self.with_content is not None:
            return f"-translate::{self.translate}\n  -with::{pformat(self.with_content)}"
        return f"-translate::{self.translate}"