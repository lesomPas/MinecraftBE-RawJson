from .classes import Text, Score, Selector, Translate, Rawtext, RawComponent
from pprint import pprint
import json

priority = {
    "translate": 4,
    "text": 3,
    "score": 2,
    "selector": 1,
    None: 0
}

def arrayProcessing(dictionary: dict) -> dict:
    results = None
    for sentence in dictionary.keys():
        if (p := priority.get(sentence, -1)) == -1:
            raise ValueError("dictionary error")
        if p >= priority[results]:
            results = sentence
    return {results: dictionary[results]} if results is not None else {}


def inRawtext(sequence: list[dict]) -> list[RawComponent]:
    if not isinstance(sequence, list):
        raise ValueError("dictionary error")
    results = []
    for sentence in sequence:
        if len(sentence) > 1 and not ("translate" in sentence and "with" in sentence):
            sentence = arrayProcessing(sentence)

        if "text" in sentence:
            results.append(Text.toText(sentence))
        elif "score" in sentence:
            results.append(Score.toScore(sentence))
        elif "selector" in sentence:
            results.append(Selector.toSelector(sentence))
        elif "translate" in sentence:
            results.append(Translate.toTranslate(sentence))
        elif "rawtext" in sentence:
            results.append(Rawtext(sentence))
        else:
            raise ValueError("dictionary error")

    return results

def process(dictionary: dict) -> dict:
    if "rawtext" not in dictionary:
        raise ValueError("dictionary error")
    return inRawtext(dictionary["rawtext"])

def main():
    Rawtext.process = staticmethod(process)
    with open("testing.json", "r", encoding="utf-8") as js:
        data = json.load(js)
    data = Rawtext(data)
    pprint(data)
    pprint(data.toDictionary())

if __name__ == '__main__':
    main()