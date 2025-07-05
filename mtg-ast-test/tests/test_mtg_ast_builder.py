"""
Unit tests for the MTG AST builder class.
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


class TestMTGCardBuilder(unittest.TestCase):
    """Test cases for the MTGCardBuilder class."""
    
    def test_add_keyword_ability(self):
        """Test adding a keyword ability to the card."""
        builder = MTGCardBuilder()
        ability = builder.add_keyword_ability("Flying", "This creature can't be blocked except by creatures with flying or reach.")
        
        self.assertIsInstance(ability, KeywordAbility)
        self.assertEqual(ability.keyword, "Flying")
        self.assertEqual(ability.reminder_text, "This creature can't be blocked except by creatures with flying or reach.")
        self.assertIn(ability, builder.root.children)
    
    def test_add_token_creation(self):
        """Test adding a token creation to the card."""
        builder = MTGCardBuilder()
        token = builder.add_token_creation(1, 1, ["white"], ["creature"], ["Cat"], 2)
        
        self.assertIsInstance(token, TokenCreation)
        self.assertEqual(token.power, 1)
        self.assertEqual(token.toughness, 1)
        self.assertEqual(token.colors, ["white"])
        self.assertEqual(token.types, ["creature"])
        self.assertEqual(token.subtypes, ["Cat"])
        self.assertEqual(token.count, 2)
        self.assertIn(token, builder.root.children)
    
    def test_add_triggered_ability(self):
        """Test adding a triggered ability to the card."""
        builder = MTGCardBuilder()
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card")
        ability = builder.add_triggered_ability("when this creature enters the battlefield", effect)
        
        self.assertIsInstance(ability, TriggeredAbility)
        self.assertEqual(ability.trigger, "when this creature enters the battlefield")
        self.assertEqual(ability.effect, effect)
        self.assertIn(ability, builder.root.children)
    
    def test_add_static_ability(self):
        """Test adding a static ability to the card."""
        builder = MTGCardBuilder()
        ability = builder.add_static_ability("get +1/+1", "creatures you control")
        
        self.assertIsInstance(ability, StaticAbility)
        self.assertEqual(ability.effect, "get +1/+1")
        self.assertEqual(ability.target, "creatures you control")
        self.assertIn(ability, builder.root.children)
    
    def test_add_conditional_effect(self):
        """Test adding a conditional effect to the card."""
        builder = MTGCardBuilder()
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card")
        else_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "discard a card")
        conditional = builder.add_conditional_effect("if you control three or more creatures", effect, else_effect)
        
        self.assertIsInstance(conditional, ConditionalEffect)
        self.assertEqual(conditional.condition, "if you control three or more creatures")
        self.assertEqual(conditional.effect, effect)
        self.assertEqual(conditional.else_effect, else_effect)
        self.assertIn(conditional, builder.root.children)
    
    def test_add_target_effect(self):
        """Test adding a targeted effect to the card."""
        builder = MTGCardBuilder()
        effect = builder.add_target_effect("gets +2/+2", "creature", ["you control"], "until end of turn")
        
        self.assertIsInstance(effect, TargetEffect)
        self.assertEqual(effect.value, "gets +2/+2")
        self.assertEqual(effect.target_type, "creature")
        self.assertEqual(effect.target_restrictions, ["you control"])
        self.assertEqual(effect.duration, "until end of turn")
        self.assertIn(effect, builder.root.children)
    
    def test_add_counter_effect(self):
        """Test adding a counter effect to the card."""
        builder = MTGCardBuilder()
        effect = builder.add_counter_effect("+1/+1", "add", 2, "target creature you control")
        
        self.assertIsInstance(effect, CounterEffect)
        self.assertEqual(effect.counter_type, "+1/+1")
        self.assertEqual(effect.action, "add")
        self.assertEqual(effect.count, 2)
        self.assertEqual(effect.target, "target creature you control")
        self.assertIn(effect, builder.root.children)
    
    def test_add_cost_modification(self):
        """Test adding a cost modification to the card."""
        builder = MTGCardBuilder()
        modification = builder.add_cost_modification("reduce", "{1}", "for each Cat you control", 
                                                   "This spell costs {1} less to cast for each Cat you control.")
        
        self.assertIsInstance(modification, CostModification)
        self.assertEqual(modification.modification_type, "reduce")
        self.assertEqual(modification.cost, "{1}")
        self.assertEqual(modification.condition, "for each Cat you control")
        self.assertEqual(modification.reminder_text, "This spell costs {1} less to cast for each Cat you control.")
        self.assertIn(modification, builder.root.children)
    
    def test_build(self):
        """Test building the MTG card AST."""
        builder = MTGCardBuilder()
        builder.add_keyword_ability("Flying")
        builder.add_keyword_ability("Vigilance")
        
        root = builder.build()
        self.assertIsInstance(root, MTGNode)
        self.assertEqual(len(root.children), 2)
        self.assertIsInstance(root.children[0], KeywordAbility)
        self.assertIsInstance(root.children[1], KeywordAbility)
    
    def test_to_dict(self):
        """Test converting the MTG card AST to a dictionary."""
        builder = MTGCardBuilder()
        builder.add_keyword_ability("Flying")
        builder.add_keyword_ability("Vigilance")
        
        card_dict = builder.to_dict()
        self.assertEqual(card_dict['type'], 'MTGCard')
        self.assertEqual(len(card_dict['children']), 2)
        self.assertEqual(card_dict['children'][0]['type'], 'KeywordAbility')
        self.assertEqual(card_dict['children'][1]['type'], 'KeywordAbility')


if __name__ == '__main__':
    unittest.main()