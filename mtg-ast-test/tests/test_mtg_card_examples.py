"""
Tests for constructing example MTG cards using the AST.

This module demonstrates how to use the MTG AST to represent real MTG cards.
"""
import sys
import os
import unittest
from typing import List, Optional, Dict, Any

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtg_ast import MTGNode, MTGDeclaration, MTGStatement, MTGExpression
from mtg_ast_specialized import (
    KeywordAbility, TokenCreation, TriggeredAbility, StaticAbility,
    ConditionalEffect, TargetEffect, CounterEffect, CostModification
)
from mtg_ast_builder import MTGCardBuilder


class TestMTGCardExamples(unittest.TestCase):
    """Test cases for constructing example MTG cards."""
    
    def test_card_with_keyword_abilities(self):
        """Test constructing a card with keyword abilities."""
        # Example: "First strike, vigilance"
        builder = MTGCardBuilder()
        builder.add_keyword_ability("First strike")
        builder.add_keyword_ability("Vigilance")
        
        card = builder.build()
        self.assertEqual(len(card.children), 2)
        self.assertIsInstance(card.children[0], KeywordAbility)
        self.assertIsInstance(card.children[1], KeywordAbility)
        self.assertEqual(card.children[0].keyword, "First strike")
        self.assertEqual(card.children[1].keyword, "Vigilance")
    
    def test_card_with_static_and_triggered_abilities(self):
        """Test constructing a card with static and triggered abilities."""
        # Example: "Other Cats you control get +1/+1.
        # Whenever ~ or another nontoken Cat you control enters, create a 1/1 white Cat creature token."
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
        
        card = builder.build()
        self.assertEqual(len(card.children), 2)
        self.assertIsInstance(card.children[0], StaticAbility)
        self.assertIsInstance(card.children[1], TriggeredAbility)
        
        # Check static ability
        static_ability = card.children[0]
        self.assertEqual(static_ability.effect, "get +1/+1")
        self.assertEqual(static_ability.target, "other Cats you control")
        
        # Check triggered ability
        triggered_ability = card.children[1]
        self.assertEqual(triggered_ability.trigger, trigger)
        self.assertEqual(triggered_ability.effect, token_effect)
        
        # Check token creation
        self.assertEqual(len(triggered_ability.children), 2)  # effect + token
        token = None
        for child in triggered_ability.children:
            if isinstance(child, TokenCreation):
                token = child
                break
        self.assertIsNotNone(token)
        self.assertEqual(token.power, 1)
        self.assertEqual(token.toughness, 1)
        self.assertEqual(token.colors, ["white"])
        self.assertEqual(token.types, ["creature"])
        self.assertEqual(token.subtypes, ["Cat"])
        self.assertEqual(token.count, 1)
    
    def test_card_with_conditional_effect(self):
        """Test constructing a card with a conditional effect."""
        # Example: "Kicker {2}{W} (You may pay an additional {2}{W} as you cast this spell.)
        # Target creature you control gains indestructible until end of turn. If this spell was kicked, 
        # instead any number of target creatures you control gain indestructible until end of turn."
        builder = MTGCardBuilder()
        
        # Cost modification: "Kicker {2}{W}"
        builder.add_cost_modification("additional", "{2}{W}", None, 
                                     "You may pay an additional {2}{W} as you cast this spell.")
        
        # Conditional effect
        condition = "if this spell was kicked"
        
        # Effect if not kicked: "Target creature you control gains indestructible until end of turn."
        normal_effect = TargetEffect("gains indestructible", "creature", ["you control"], "until end of turn")
        
        # Effect if kicked: "Any number of target creatures you control gain indestructible until end of turn."
        kicked_effect = TargetEffect("gain indestructible", "creature", ["any number", "you control"], "until end of turn")
        
        # Add the conditional effect
        builder.add_conditional_effect(condition, kicked_effect, normal_effect)
        
        card = builder.build()
        self.assertEqual(len(card.children), 2)
        self.assertIsInstance(card.children[0], CostModification)
        self.assertIsInstance(card.children[1], ConditionalEffect)
        
        # Check cost modification
        cost_mod = card.children[0]
        self.assertEqual(cost_mod.modification_type, "additional")
        self.assertEqual(cost_mod.cost, "{2}{W}")
        self.assertEqual(cost_mod.reminder_text, "You may pay an additional {2}{W} as you cast this spell.")
        
        # Check conditional effect
        conditional = card.children[1]
        self.assertEqual(conditional.condition, condition)
        
        # Check effects
        self.assertIsInstance(conditional.effect, TargetEffect)
        self.assertIsInstance(conditional.else_effect, TargetEffect)
        
        # Check kicked effect
        kicked = conditional.effect
        self.assertEqual(kicked.value, "gain indestructible")
        self.assertEqual(kicked.target_type, "creature")
        self.assertEqual(kicked.target_restrictions, ["any number", "you control"])
        self.assertEqual(kicked.duration, "until end of turn")
        
        # Check normal effect
        normal = conditional.else_effect
        self.assertEqual(normal.value, "gains indestructible")
        self.assertEqual(normal.target_type, "creature")
        self.assertEqual(normal.target_restrictions, ["you control"])
        self.assertEqual(normal.duration, "until end of turn")
    
    def test_card_with_multiple_triggered_abilities(self):
        """Test constructing a card with multiple triggered abilities."""
        # Example: "Flying
        # Whenever you gain life, put a +1/+1 counter on this creature.
        # Whenever you put one or more +1/+1 counters on this creature, draw 1 card. This ability triggers only once each turn."
        builder = MTGCardBuilder()
        
        # Keyword ability: "Flying"
        builder.add_keyword_ability("Flying")
        
        # Triggered ability 1: "Whenever you gain life, put a +1/+1 counter on this creature."
        trigger1 = "whenever you gain life"
        counter_effect = CounterEffect("+1/+1", "add", 1, "this creature")
        builder.add_triggered_ability(trigger1, counter_effect)
        
        # Triggered ability 2: "Whenever you put one or more +1/+1 counters on this creature, draw 1 card. This ability triggers only once each turn."
        trigger2 = "whenever you put one or more +1/+1 counters on this creature"
        draw_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
        triggered_ability2 = builder.add_triggered_ability(trigger2, draw_effect)
        
        # Add restriction to triggered ability 2
        restriction = MTGExpression(MTGExpression.ExpressionType.EFFECT, "triggers only once each turn")
        triggered_ability2.add_child(restriction)
        
        card = builder.build()
        self.assertEqual(len(card.children), 3)
        self.assertIsInstance(card.children[0], KeywordAbility)
        self.assertIsInstance(card.children[1], TriggeredAbility)
        self.assertIsInstance(card.children[2], TriggeredAbility)
        
        # Check keyword ability
        keyword = card.children[0]
        self.assertEqual(keyword.keyword, "Flying")
        
        # Check triggered ability 1
        triggered1 = card.children[1]
        self.assertEqual(triggered1.trigger, trigger1)
        self.assertIsInstance(triggered1.effect, CounterEffect)
        
        counter = triggered1.effect
        self.assertEqual(counter.counter_type, "+1/+1")
        self.assertEqual(counter.action, "add")
        self.assertEqual(counter.count, 1)
        self.assertEqual(counter.target, "this creature")
        
        # Check triggered ability 2
        triggered2 = card.children[2]
        self.assertEqual(triggered2.trigger, trigger2)
        self.assertEqual(triggered2.effect, draw_effect)
        
        # Check restriction
        self.assertEqual(len(triggered2.children), 2)  # effect + restriction
        restriction_found = False
        for child in triggered2.children:
            if (isinstance(child, MTGExpression) and 
                child.expression_type == MTGExpression.ExpressionType.EFFECT and 
                child.value == "triggers only once each turn"):
                restriction_found = True
                break
        self.assertTrue(restriction_found)
    
    def test_card_with_token_creation(self):
        """Test constructing a card with token creation."""
        # Example: "Lifelink
        # When this creature enters, create two 3/3 white Knight creature tokens."
        builder = MTGCardBuilder()
        
        # Keyword ability: "Lifelink"
        builder.add_keyword_ability("Lifelink")
        
        # Triggered ability: "When this creature enters, create two 3/3 white Knight creature tokens."
        trigger = "when this creature enters"
        token_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "create tokens")
        triggered_ability = builder.add_triggered_ability(trigger, token_effect)
        
        # Add the token creation as a child of the triggered ability
        token = TokenCreation(3, 3, ["white"], ["creature"], ["Knight"], 2)
        triggered_ability.add_child(token)
        
        card = builder.build()
        self.assertEqual(len(card.children), 2)
        self.assertIsInstance(card.children[0], KeywordAbility)
        self.assertIsInstance(card.children[1], TriggeredAbility)
        
        # Check keyword ability
        keyword = card.children[0]
        self.assertEqual(keyword.keyword, "Lifelink")
        
        # Check triggered ability
        triggered = card.children[1]
        self.assertEqual(triggered.trigger, trigger)
        
        # Check token creation
        self.assertEqual(len(triggered.children), 2)  # effect + token
        token = None
        for child in triggered.children:
            if isinstance(child, TokenCreation):
                token = child
                break
        self.assertIsNotNone(token)
        self.assertEqual(token.power, 3)
        self.assertEqual(token.toughness, 3)
        self.assertEqual(token.colors, ["white"])
        self.assertEqual(token.types, ["creature"])
        self.assertEqual(token.subtypes, ["Knight"])
        self.assertEqual(token.count, 2)


if __name__ == '__main__':
    unittest.main()