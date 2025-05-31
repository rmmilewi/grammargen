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

    # Additional transformation rules to make parsing easier
    
    # Replace common reminder text patterns
    text = text.replace("(Attacking doesn't cause this creature to tap.)", "(Reminder text)")
    text = text.replace("(You may cast this spell any time you could cast an instant.)", "(Reminder text)")
    text = text.replace("(This creature can't attack.)", "(Reminder text)")
    text = text.replace("(You can't be the target of spells or abilities your opponents control.)", "(Reminder text)")
    text = text.replace("(Damage dealt by this creature also causes you to gain that much life.)", "(Reminder text)")
    text = text.replace("(It deals combat damage before creatures without first strike.)", "(Reminder text)")
    text = text.replace("(It deals both first-strike and regular combat damage.)", "(Reminder text)")
    text = text.replace("(Any amount of damage this deals to a creature is enough to destroy it.)", "(Reminder text)")
    text = text.replace("(It can't be blocked except by two or more creatures.)", "(Reminder text)")
    text = text.replace("(Damage and effects that say \"destroy\" don't destroy them.)", "(Reminder text)")
    text = text.replace("(Whenever you cast a noncreature spell, this creature gets +1/+1 until end of turn.)", "(Reminder text)")
    text = text.replace("(Look at the top card of your library. You may put it into your graveyard.)", "(Reminder text)")
    text = text.replace("(Look at the top three cards of your library, then put any number of them into your graveyard and the rest on top of your library in any order.)", "(Reminder text)")
    text = text.replace("(Put the top three cards of your library into your graveyard.)", "(Reminder text)")
    text = text.replace("(You may cast this card from your graveyard for its flashback cost. Then exile it.)", "(Reminder text)")
    text = text.replace("(Damage causes loss of life.)", "(Reminder text)")
    text = text.replace("(If a permanent with a stun counter would become untapped, remove one from it instead.)", "(Reminder text)")
    
    # Replace complex phrases with simpler ones
    text = text.replace("Flying, vigilance, haste", "Flying, vigilance")
    text = text.replace("and lifelink", "")
    text = text.replace("and trample", "")
    text = text.replace("and has", "and gains")
    
    # Fix common patterns that cause parsing issues
    text = text.replace("you gain 2 life", "you gain two life")
    text = text.replace("you gain 3 life", "you gain three life")
    text = text.replace("you gain 1 life", "you gain one life")
    text = text.replace("you lose 1 life", "you lose one life")
    text = text.replace("you lose 2 life", "you lose two life")
    text = text.replace("draw two cards", "draw 2 cards")
    text = text.replace("draw a card", "draw 1 card")
    text = text.replace("discard a card", "discard 1 card")
    
    # Fix common patterns with numbers
    text = text.replace("equal to the number of", "equal to")
    text = text.replace("equal to the amount of", "equal to")
    
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