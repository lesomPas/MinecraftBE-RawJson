from classes import RawText, RawScore, RawSelector, RawTranslate, Rawtext, RawComponent
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
            results.append(RawText(sentence))
        elif "score" in sentence:
            results.append(RawScore(sentence))
        elif "selector" in sentence:
            results.append(RawSelector(sentence))
        elif "translate" in sentence:
            results.append(RawTranslate(sentence))
        elif "rawtext" in sentence:
            results.append(Rawtext(sentence))
        else:
            raise ValueError("dictionary error")

    return results

def process(dictionary: dict) -> dict:
    if "rawtext" not in dictionary:
        raise ValueError("dictionary error")
    return inRawtext(dictionary["rawtext"])

Rawtext.process = process

def main():
    with open("testing.json", "r", encoding="utf-8") as js:
        data = json.load(js)
    data = Rawtext(data)
    pprint(data)

if __name__ == '__main__':
    main()