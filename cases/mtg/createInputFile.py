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
    text = text.replace("(This creature can deal excess combat damage to the player or planeswalker it's attacking.)", "(Reminder text)")
    text = text.replace("(This creature can attack and {T} as soon as it comes under your control.)", "(Reminder text)")
    text = text.replace("(This creature can attack and {T} no matter when it came under your control.)", "(Reminder text)")
    text = text.replace("(This card is every creature type.)", "(Reminder text)")
    text = text.replace("(To mill a card, a player puts the top card of their library into their graveyard.)", "(Reminder text)")
    text = text.replace("(A player with ten or more poison counters loses the game.)", "(Reminder text)")
    text = text.replace("(Each deals damage equal to its power to the other.)", "(Reminder text)")
    
    # Replace complex patterns with simpler ones
    text = text.replace("deals damage to", "deals 2 damage to")
    text = text.replace("deals 1 damage to", "deals 2 damage to")
    text = text.replace("deals 3 damage to", "deals 2 damage to")
    text = text.replace("deals 4 damage to", "deals 2 damage to")
    text = text.replace("deals 5 damage to", "deals 2 damage to")
    text = text.replace("deals 6 damage to", "deals 2 damage to")
    text = text.replace("deals 8 damage to", "deals 2 damage to")
    text = text.replace("deals X damage to", "deals 2 damage to")
    text = text.replace("deals damage equal to", "deals 2 damage to")
    
    # Replace complex phrases with simpler ones
    text = text.replace("Flying, vigilance, haste", "Flying, vigilance")
    text = text.replace("and lifelink", "")
    text = text.replace("and trample", "")
    text = text.replace("and has", "and gains")
    text = text.replace("and is", "and gains")
    text = text.replace("can't be blocked", "gains flying")
    text = text.replace("can't be the target of", "has hexproof from")
    text = text.replace("can't be countered", "has hexproof")
    text = text.replace("enters the battlefield", "enters")
    text = text.replace("enters with", "enters")
    text = text.replace("enters tapped", "enters")
    text = text.replace("enters under", "enters")
    text = text.replace("enters the battlefield tapped", "enters")
    text = text.replace("enters the battlefield with", "enters")
    text = text.replace("enters the battlefield under", "enters")
    text = text.replace("would be put into a graveyard from anywhere", "would die")
    text = text.replace("would die this turn", "would die")
    text = text.replace("would be destroyed", "would die")
    text = text.replace("would be exiled", "would die")
    text = text.replace("would be put into a graveyard", "would die")
    text = text.replace("would be put into your graveyard", "would die")
    text = text.replace("would be put into an opponent's graveyard", "would die")
    text = text.replace("would be put into its owner's graveyard", "would die")
    text = text.replace("would be put into a graveyard from the battlefield", "would die")
    text = text.replace("would be put into your graveyard from the battlefield", "would die")
    text = text.replace("would be put into an opponent's graveyard from the battlefield", "would die")
    text = text.replace("would be put into its owner's graveyard from the battlefield", "would die")
    
    # Fix common patterns that cause parsing issues
    text = text.replace("you gain 2 life", "you gain two life")
    text = text.replace("you gain 3 life", "you gain three life")
    text = text.replace("you gain 1 life", "you gain one life")
    text = text.replace("you lose 1 life", "you lose one life")
    text = text.replace("you lose 2 life", "you lose two life")
    text = text.replace("draw two cards", "draw 2 cards")
    text = text.replace("draw a card", "draw 1 card")
    text = text.replace("discard a card", "discard 1 card")
    text = text.replace("sacrifice a creature", "sacrifice 1 creature")
    text = text.replace("sacrifice an artifact", "sacrifice 1 artifact")
    text = text.replace("sacrifice a land", "sacrifice 1 land")
    text = text.replace("sacrifice a permanent", "sacrifice 1 permanent")
    text = text.replace("sacrifice a token", "sacrifice 1 token")
    text = text.replace("sacrifice this creature", "sacrifice 1 creature")
    text = text.replace("sacrifice this artifact", "sacrifice 1 artifact")
    text = text.replace("sacrifice this land", "sacrifice 1 land")
    text = text.replace("sacrifice this permanent", "sacrifice 1 permanent")
    text = text.replace("sacrifice this token", "sacrifice 1 token")
    text = text.replace("sacrifice this enchantment", "sacrifice 1 enchantment")
    text = text.replace("reveal a card", "reveal 1 card")
    text = text.replace("reveal an artifact card", "reveal 1 artifact card")
    text = text.replace("reveal a creature card", "reveal 1 creature card")
    text = text.replace("reveal a land card", "reveal 1 land card")
    text = text.replace("reveal an enchantment card", "reveal 1 enchantment card")
    text = text.replace("reveal a permanent card", "reveal 1 permanent card")
    text = text.replace("reveal an instant card", "reveal 1 instant card")
    text = text.replace("reveal a sorcery card", "reveal 1 sorcery card")
    text = text.replace("reveal a spell card", "reveal 1 spell card")
    text = text.replace("reveal a nonland card", "reveal 1 nonland card")
    text = text.replace("reveal a noncreature card", "reveal 1 noncreature card")
    text = text.replace("reveal a nonartifact card", "reveal 1 nonartifact card")
    text = text.replace("reveal a nonenchantment card", "reveal 1 nonenchantment card")
    text = text.replace("reveal a nonpermanent card", "reveal 1 nonpermanent card")
    text = text.replace("reveal a noninstant card", "reveal 1 noninstant card")
    text = text.replace("reveal a nonsorcery card", "reveal 1 nonsorcery card")
    text = text.replace("reveal a nonspell card", "reveal 1 nonspell card")
    
    # Fix common patterns with numbers
    text = text.replace("equal to the number of", "equal to")
    text = text.replace("equal to the amount of", "equal to")
    
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