"""
Example script demonstrating how to use the MTG AST to represent a real MTG card.
"""
import json
from mtg_ast import MTGExpression
from mtg_ast_specialized import TokenCreation
from mtg_ast_builder import MTGCardBuilder


def create_example_card():
    """
    Create an example MTG card AST.
    
    This function demonstrates how to use the MTG AST to represent a real MTG card.
    The example card has the following text:
    
    "Flying
    Whenever you gain life, put a +1/+1 counter on this creature.
    Whenever you put one or more +1/+1 counters on this creature, draw 1 card. 
    This ability triggers only once each turn."
    
    Returns:
        A dictionary representation of the card AST.
    """
    # Create a builder
    builder = MTGCardBuilder()
    
    # Keyword ability: "Flying"
    builder.add_keyword_ability("Flying")
    
    # Triggered ability 1: "Whenever you gain life, put a +1/+1 counter on this creature."
    trigger1 = "whenever you gain life"
    counter_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "put a +1/+1 counter", "this creature")
    builder.add_triggered_ability(trigger1, counter_effect)
    
    # Triggered ability 2: "Whenever you put one or more +1/+1 counters on this creature, draw 1 card. This ability triggers only once each turn."
    trigger2 = "whenever you put one or more +1/+1 counters on this creature"
    draw_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
    triggered_ability2 = builder.add_triggered_ability(trigger2, draw_effect)
    
    # Add restriction to triggered ability 2
    restriction = MTGExpression(MTGExpression.ExpressionType.EFFECT, "triggers only once each turn")
    triggered_ability2.add_child(restriction)
    
    # Build the AST
    card_ast = builder.build()
    
    # Convert to dictionary representation
    return builder.to_dict()


def create_cat_lord_card():
    """
    Create an example MTG card AST for a "Cat Lord" card.
    
    This function demonstrates how to use the MTG AST to represent a real MTG card.
    The example card has the following text:
    
    "Other Cats you control get +1/+1.
    Whenever ~ or another nontoken Cat you control enters, create a 1/1 white Cat creature token."
    
    Returns:
        A dictionary representation of the card AST.
    """
    # Create a builder
    builder = MTGCardBuilder()
    
    # Static ability: "Other Cats you control get +1/+1."
    builder.add_static_ability("get +1/+1", "other Cats you control")
    
    # Triggered ability: "Whenever ~ or another nontoken Cat you control enters, create a 1/1 white Cat creature token."
    trigger = "whenever ~ or another nontoken Cat you control enters"
    token_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "create a token")
    triggered_ability = builder.add_triggered_ability(trigger, token_effect)
    
    # Add the token creation as a child of the triggered ability
    token = TokenCreation(1, 1, ["white"], ["creature"], ["Cat"], 1)
    triggered_ability.add_child(token)
    
    # Build the AST
    card_ast = builder.build()
    
    # Convert to dictionary representation
    return builder.to_dict()


def create_conditional_card():
    """
    Create an example MTG card AST with a conditional effect.
    
    This function demonstrates how to use the MTG AST to represent a real MTG card.
    The example card has the following text:
    
    "Kicker {2}{W} (You may pay an additional {2}{W} as you cast this spell.)
    Target creature you control gains indestructible until end of turn. If this spell was kicked, 
    instead any number of target creatures you control gain indestructible until end of turn."
    
    Returns:
        A dictionary representation of the card AST.
    """
    # Create a builder
    builder = MTGCardBuilder()
    
    # Cost modification: "Kicker {2}{W}"
    builder.add_cost_modification("additional", "{2}{W}", None, 
                                 "You may pay an additional {2}{W} as you cast this spell.")
    
    # Conditional effect
    condition = "if this spell was kicked"
    
    # Effect if not kicked: "Target creature you control gains indestructible until end of turn."
    normal_effect = MTGExpression(MTGExpression.ExpressionType.EFFECT, "gains indestructible", "target creature you control")
    duration1 = MTGExpression(MTGExpression.ExpressionType.DURATION, "until end of turn")
    normal_effect.add_child(duration1)
    
    # Effect if kicked: "Any number of target creatures you control gain indestructible until end of turn."
    kicked_effect = MTGExpression(MTGExpression.ExpressionType.EFFECT, "gain indestructible", "any number of target creatures you control")
    duration2 = MTGExpression(MTGExpression.ExpressionType.DURATION, "until end of turn")
    kicked_effect.add_child(duration2)
    
    # Add the conditional effect
    builder.add_conditional_effect(condition, kicked_effect, normal_effect)
    
    # Build the AST
    card_ast = builder.build()
    
    # Convert to dictionary representation
    return builder.to_dict()


if __name__ == "__main__":
    # Create example cards
    example_card = create_example_card()
    cat_lord_card = create_cat_lord_card()
    conditional_card = create_conditional_card()
    
    # Print the cards as JSON
    print("Example Card:")
    print(json.dumps(example_card, indent=2))
    print("\nCat Lord Card:")
    print(json.dumps(cat_lord_card, indent=2))
    print("\nConditional Card:")
    print(json.dumps(conditional_card, indent=2))