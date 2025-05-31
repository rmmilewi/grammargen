import json

def cleanUpCardText(card):
    text = card["text"]
    name = card["name"]
    if name is not None:
        if "," in name:
            splitName = name.split(",")
            text = text.replace(name, "~f")
            text = text.replace(splitName[0], "~")
        else:
            text = text.replace(name, "~")
    return f'"""{text}"""\n'


def extract_english_card_text(json_path, output_path="inputs.txt"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data.get("data", []).get("cards",[])

    with open(output_path, "w", encoding="utf-8") as out:
        for card in cards:
            if card.get("language") == "English" and "text" in card:
                cardTextOutput = cleanUpCardText(card)
                print(cardTextOutput)
                out.write(cardTextOutput)

# Usage
extract_english_card_text("FDN.json")