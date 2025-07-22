from utils import is_single_string_value, is_single_dictionary_value, is_string_value
from pprint import pformat
from typing import Union, List, Dict, Any


class RawComponent:
    """Base class for all raw component types."""
    def with_id(self) -> str:
        """Return a unique identifier for the component."""
        return f"{id(self)}::{str(self)}"

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Rawtext(RawComponent):
    """Class for handling raw text components."""
    process = None  # Placeholder for processing function

    def __init__(self, dictionary: dict) -> None:
        self.data = Rawtext.process(dictionary) # if self.process else dictionary

    def __str__(self) -> str:
        return pformat(self.data)

    def __repr__(self) -> str:
        return f"-rawtext::{str(self)}"


class RawText(RawComponent):
    """Class for handling simple text components."""
    def __init__(self, dictionary: dict) -> None:
        if not is_single_string_value(dictionary, "text"):
            raise ValueError("Invalid dictionary: must contain single 'text' string value")
        self.content = dictionary["text"]

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return f"-text::{str(self)}"


class RawScore(RawComponent):
    """Class for handling score components."""
    def __init__(self, dictionary: dict) -> None:
        if not is_single_dictionary_value(dictionary, "score"):
            raise ValueError("Invalid dictionary: must contain single 'score' dictionary value")

        data = dictionary["score"]
        if not is_string_value(data, ["name", "objective"]):
            raise ValueError("Score dictionary must contain 'name' and 'objective' string values")

        self.name = data["name"]
        self.objective = data["objective"]

    def __str__(self) -> str:
        return f"{self.name} >> {self.objective}"

    def __repr__(self) -> str:
        return f"-score::{str(self)}"


class RawSelector(RawComponent):
    """Class for handling selector components."""
    def __init__(self, dictionary: dict) -> None:
        if not is_single_string_value(dictionary, "selector"):
            raise ValueError("Invalid dictionary: must contain single 'selector' string value")
        self.content = dictionary["selector"]

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return f"-selector::{str(self)}"


class RawTranslate(RawComponent):
    """Class for handling translation components."""
    def __init__(self, dictionary: dict) -> None:
        if "translate" not in dictionary:
            raise ValueError("Dictionary must contain 'translate' key")
        
        if not isinstance(dictionary["translate"], str):
            raise ValueError("'translate' value must be a string")

        self.translate = dictionary["translate"]
        self.with_content: Union[List[str], Rawtext, None] = None

        if "with" not in dictionary:
            if len(dictionary) > 1:
                raise ValueError("Dictionary contains extra keys")
            return

        if len(dictionary) > 2:
            raise ValueError("Dictionary contains extra keys")

        with_value = dictionary["with"]
        if isinstance(with_value, list) and all(isinstance(i, str) for i in with_value):
            self.with_content = with_value
        elif isinstance(with_value, dict):
            self.with_content = Rawtext(with_value)
        else:
            raise ValueError("'with' must be a list of strings or a dictionary")

    def __str__(self) -> str:
        if self.with_content:
            return f"{self.translate}\n  {pformat(self.with_content)}"
        return self.translate

    def __repr__(self) -> str:
        return f"-translate::{self.translate}\n  -with::{pformat(self.with_content)}"