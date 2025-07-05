"""
Example script demonstrating the new MTG AST functionality with specific cards.
"""
import json
from mtg_ast import MTGExpression
from mtg_ast_specialized import TokenCreation
from mtg_ast_builder import MTGCardBuilder


def create_elf_lord_card():
    """
    Create an Elf lord card AST.
    
    Card text: "Other Elf creatures you control get +1/+1.
    {T}: Add {G} for each Elf you control."
    
    Returns:
        A dictionary representation of the card AST.
    """
    builder = MTGCardBuilder()
    
    # Static ability: "Other Elf creatures you control get +1/+1."
    builder.add_static_ability("get +1/+1", "other Elf creatures you control")
    
    # Activated ability: "{T}: Add {G} for each Elf you control."
    builder.add_activated_ability("{T}", "Add {G} for each Elf you control")
    
    return builder.to_dict()


def create_enchantment_with_conditional_trigger():
    """
    Create an enchantment with conditional triggered abilities.
    
    Card text: "When this enchantment enters, if you control a creature with power 4 or greater, draw 1 card.
    Creatures you control have trample. (Each of those creatures can deal excess combat damage to the player or planeswalker it's attacking.)
    Whenever a creature you control with power 4 or greater enters, draw 1 card."
    
    Returns:
        A dictionary representation of the card AST.
    """
    builder = MTGCardBuilder()
    
    # Conditional triggered ability: "When this enchantment enters, if you control a creature with power 4 or greater, draw 1 card."
    trigger1 = "when this enchantment enters"
    condition1 = "if you control a creature with power 4 or greater"
    effect1 = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
    builder.add_conditional_triggered_ability(trigger1, condition1, effect1)
    
    # Static ability with reminder text: "Creatures you control have trample."
    builder.add_keyword_ability("Trample", 
                               "Each of those creatures can deal excess combat damage to the player or planeswalker it's attacking.",
                               target="creatures you control")
    
    # Regular triggered ability: "Whenever a creature you control with power 4 or greater enters, draw 1 card."
    trigger2 = "whenever a creature you control with power 4 or greater enters"
    effect2 = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
    builder.add_triggered_ability(trigger2, effect2)
    
    return builder.to_dict()


def create_spell_with_sequential_effects():
    """
    Create a spell with sequential effects.
    
    Card text: "Reveal the top X cards of your library. You may put any number of permanent cards with mana value X or less from among them onto the battlefield. Then put all cards revealed this way that weren't put onto the battlefield into your graveyard."
    
    Returns:
        A dictionary representation of the card AST.
    """
    builder = MTGCardBuilder()
    
    # This spell has sequential effects that need to be represented as a sequence
    builder.add_spell_sequence([
        {
            "type": "reveal",
            "target": "top X cards of your library",
            "zone": "library"
        },
        {
            "type": "optional_put",
            "source": "revealed cards",
            "target": "battlefield",
            "restriction": "permanent cards with mana value X or less"
        },
        {
            "type": "put",
            "source": "remaining revealed cards",
            "target": "graveyard"
        }
    ])
    
    return builder.to_dict()


def create_spell_with_variable_cost_reduction():
    """
    Create a spell with variable cost reduction.
    
    Card text: "This spell costs {X} less to cast, where X is the total power of creatures you control.
    Trample (Reminder text)"
    
    Returns:
        A dictionary representation of the card AST.
    """
    builder = MTGCardBuilder()
    
    # Variable cost modification
    builder.add_variable_cost_modification(
        modification_type="reduce",
        cost="{X}",
        variable_definition="where X is the total power of creatures you control"
    )
    
    # Keyword ability with reminder text
    builder.add_keyword_ability("Trample", "Reminder text")
    
    return builder.to_dict()


if __name__ == "__main__":
    # Create example cards
    elf_lord = create_elf_lord_card()
    enchantment = create_enchantment_with_conditional_trigger()
    spell_sequence = create_spell_with_sequential_effects()
    variable_cost = create_spell_with_variable_cost_reduction()
    
    # Print the cards as JSON
    print("Elf Lord Card:")
    print(json.dumps(elf_lord, indent=2))
    print("\nEnchantment with Conditional Trigger:")
    print(json.dumps(enchantment, indent=2))
    print("\nSpell with Sequential Effects:")
    print(json.dumps(spell_sequence, indent=2))
    print("\nSpell with Variable Cost Reduction:")
    print(json.dumps(variable_cost, indent=2))