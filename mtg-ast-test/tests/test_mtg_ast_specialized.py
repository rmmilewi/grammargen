"""
Unit tests for the specialized MTG AST classes.
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


class TestKeywordAbility(unittest.TestCase):
    """Test cases for the KeywordAbility class."""
    
    def test_initialization(self):
        """Test initializing a keyword ability."""
        ability = KeywordAbility("Flying", "This creature can't be blocked except by creatures with flying or reach.")
        
        self.assertEqual(ability.keyword, "Flying")
        self.assertEqual(ability.reminder_text, "This creature can't be blocked except by creatures with flying or reach.")
        self.assertEqual(ability.declaration_type, "keyword_ability")
    
    def test_setters(self):
        """Test setting keyword ability properties."""
        ability = KeywordAbility("Flying")
        ability.keyword = "First strike"
        ability.reminder_text = "This creature deals combat damage before creatures without first strike."
        
        self.assertEqual(ability.keyword, "First strike")
        self.assertEqual(ability.reminder_text, "This creature deals combat damage before creatures without first strike.")
    
    def test_to_dict(self):
        """Test converting a keyword ability to a dictionary."""
        ability = KeywordAbility("Flying", "This creature can't be blocked except by creatures with flying or reach.")
        
        ability_dict = ability.to_dict()
        self.assertEqual(ability_dict['type'], 'KeywordAbility')
        self.assertEqual(ability_dict['keyword'], 'Flying')
        self.assertEqual(ability_dict['reminder_text'], "This creature can't be blocked except by creatures with flying or reach.")


class TestTokenCreation(unittest.TestCase):
    """Test cases for the TokenCreation class."""
    
    def test_initialization(self):
        """Test initializing a token creation."""
        token = TokenCreation(1, 1, ["white"], ["creature"], ["Cat"], 2)
        
        self.assertEqual(token.power, 1)
        self.assertEqual(token.toughness, 1)
        self.assertEqual(token.colors, ["white"])
        self.assertEqual(token.types, ["creature"])
        self.assertEqual(token.subtypes, ["Cat"])
        self.assertEqual(token.count, 2)
        self.assertEqual(token.declaration_type, "token_creation")
    
    def test_setters(self):
        """Test setting token creation properties."""
        token = TokenCreation(1, 1, ["white"], ["creature"], ["Cat"], 2)
        token.power = 3
        token.toughness = 3
        token.colors = ["white", "blue"]
        token.types = ["creature", "artifact"]
        token.subtypes = ["Soldier"]
        token.count = 1
        
        self.assertEqual(token.power, 3)
        self.assertEqual(token.toughness, 3)
        self.assertEqual(token.colors, ["white", "blue"])
        self.assertEqual(token.types, ["creature", "artifact"])
        self.assertEqual(token.subtypes, ["Soldier"])
        self.assertEqual(token.count, 1)
    
    def test_to_dict(self):
        """Test converting a token creation to a dictionary."""
        token = TokenCreation(1, 1, ["white"], ["creature"], ["Cat"], 2)
        
        token_dict = token.to_dict()
        self.assertEqual(token_dict['type'], 'TokenCreation')
        self.assertEqual(token_dict['power'], 1)
        self.assertEqual(token_dict['toughness'], 1)
        self.assertEqual(token_dict['colors'], ["white"])
        self.assertEqual(token_dict['types'], ["creature"])
        self.assertEqual(token_dict['subtypes'], ["Cat"])
        self.assertEqual(token_dict['count'], 2)


class TestTriggeredAbility(unittest.TestCase):
    """Test cases for the TriggeredAbility class."""
    
    def test_initialization(self):
        """Test initializing a triggered ability."""
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card")
        ability = TriggeredAbility("when this creature enters the battlefield", effect)
        
        self.assertEqual(ability.trigger, "when this creature enters the battlefield")
        self.assertEqual(ability.effect, effect)
        self.assertEqual(ability.statement_type, MTGStatement.StatementType.TRIGGERED_ABILITY)
    
    def test_initialization_without_effect(self):
        """Test initializing a triggered ability without an effect."""
        ability = TriggeredAbility("when this creature enters the battlefield")
        
        self.assertEqual(ability.trigger, "when this creature enters the battlefield")
        self.assertIsNone(ability.effect)
    
    def test_set_effect(self):
        """Test setting the effect of a triggered ability."""
        ability = TriggeredAbility("when this creature enters the battlefield")
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card")
        ability.set_effect(effect)
        
        self.assertEqual(ability.effect, effect)
        self.assertIn(effect, ability.children)
    
    def test_to_dict(self):
        """Test converting a triggered ability to a dictionary."""
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card")
        ability = TriggeredAbility("when this creature enters the battlefield", effect)
        
        ability_dict = ability.to_dict()
        self.assertEqual(ability_dict['type'], 'TriggeredAbility')
        self.assertEqual(ability_dict['trigger'], "when this creature enters the battlefield")
        self.assertEqual(len(ability_dict['children']), 1)


class TestStaticAbility(unittest.TestCase):
    """Test cases for the StaticAbility class."""
    
    def test_initialization(self):
        """Test initializing a static ability."""
        ability = StaticAbility("get +1/+1", "creatures you control")
        
        self.assertEqual(ability.effect, "get +1/+1")
        self.assertEqual(ability.target, "creatures you control")
        self.assertEqual(ability.statement_type, MTGStatement.StatementType.STATIC_ABILITY)
    
    def test_setters(self):
        """Test setting static ability properties."""
        ability = StaticAbility("get +1/+1", "creatures you control")
        ability.effect = "have hexproof"
        ability.target = "you"
        
        self.assertEqual(ability.effect, "have hexproof")
        self.assertEqual(ability.target, "you")
    
    def test_to_dict(self):
        """Test converting a static ability to a dictionary."""
        ability = StaticAbility("get +1/+1", "creatures you control")
        
        ability_dict = ability.to_dict()
        self.assertEqual(ability_dict['type'], 'StaticAbility')
        self.assertEqual(ability_dict['effect'], "get +1/+1")
        self.assertEqual(ability_dict['target'], "creatures you control")


class TestConditionalEffect(unittest.TestCase):
    """Test cases for the ConditionalEffect class."""
    
    def test_initialization(self):
        """Test initializing a conditional effect."""
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card")
        else_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "discard a card")
        conditional = ConditionalEffect("if you control three or more creatures", effect, else_effect)
        
        self.assertEqual(conditional.condition, "if you control three or more creatures")
        self.assertEqual(conditional.effect, effect)
        self.assertEqual(conditional.else_effect, else_effect)
        self.assertEqual(conditional.statement_type, MTGStatement.StatementType.CONDITIONAL)
    
    def test_initialization_without_effects(self):
        """Test initializing a conditional effect without effects."""
        conditional = ConditionalEffect("if you control three or more creatures")
        
        self.assertEqual(conditional.condition, "if you control three or more creatures")
        self.assertIsNone(conditional.effect)
        self.assertIsNone(conditional.else_effect)
    
    def test_set_effect(self):
        """Test setting the effect of a conditional effect."""
        conditional = ConditionalEffect("if you control three or more creatures")
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card")
        conditional.set_effect(effect)
        
        self.assertEqual(conditional.effect, effect)
        self.assertIn(effect, conditional.children)
    
    def test_set_else_effect(self):
        """Test setting the else effect of a conditional effect."""
        conditional = ConditionalEffect("if you control three or more creatures")
        else_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "discard a card")
        conditional.set_else_effect(else_effect)
        
        self.assertEqual(conditional.else_effect, else_effect)
        self.assertIn(else_effect, conditional.children)
        self.assertTrue(getattr(else_effect, '_is_else', False))
    
    def test_to_dict(self):
        """Test converting a conditional effect to a dictionary."""
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card")
        else_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "discard a card")
        conditional = ConditionalEffect("if you control three or more creatures", effect, else_effect)
        
        conditional_dict = conditional.to_dict()
        self.assertEqual(conditional_dict['type'], 'ConditionalEffect')
        self.assertEqual(conditional_dict['condition'], "if you control three or more creatures")
        self.assertTrue(conditional_dict['has_else'])
        self.assertEqual(len(conditional_dict['children']), 2)


class TestTargetEffect(unittest.TestCase):
    """Test cases for the TargetEffect class."""
    
    def test_initialization(self):
        """Test initializing a targeted effect."""
        effect = TargetEffect("gets +2/+2", "creature", ["you control"], "until end of turn")
        
        self.assertEqual(effect.value, "gets +2/+2")
        self.assertEqual(effect.target_type, "creature")
        self.assertEqual(effect.target_restrictions, ["you control"])
        self.assertEqual(effect.duration, "until end of turn")
        self.assertEqual(effect.expression_type, MTGExpression.ExpressionType.EFFECT)
    
    def test_setters(self):
        """Test setting targeted effect properties."""
        effect = TargetEffect("gets +2/+2", "creature", ["you control"], "until end of turn")
        effect.value = "gains flying"
        effect.target_type = "creature"
        effect.target_restrictions = ["with power 2 or less"]
        effect.duration = "until your next turn"
        
        self.assertEqual(effect.value, "gains flying")
        self.assertEqual(effect.target_type, "creature")
        self.assertEqual(effect.target_restrictions, ["with power 2 or less"])
        self.assertEqual(effect.duration, "until your next turn")
    
    def test_update_target(self):
        """Test updating the target description."""
        effect = TargetEffect("gets +2/+2", "creature", ["you control"], "until end of turn")
        effect.target_type = "player"
        effect.target_restrictions = ["opponent"]
        
        self.assertEqual(effect.target, "player opponent")
    
    def test_to_dict(self):
        """Test converting a targeted effect to a dictionary."""
        effect = TargetEffect("gets +2/+2", "creature", ["you control"], "until end of turn")
        
        effect_dict = effect.to_dict()
        self.assertEqual(effect_dict['type'], 'TargetEffect')
        self.assertEqual(effect_dict['value'], "gets +2/+2")
        self.assertEqual(effect_dict['target_type'], "creature")
        self.assertEqual(effect_dict['target_restrictions'], ["you control"])
        self.assertEqual(effect_dict['duration'], "until end of turn")


class TestCounterEffect(unittest.TestCase):
    """Test cases for the CounterEffect class."""
    
    def test_initialization(self):
        """Test initializing a counter effect."""
        effect = CounterEffect("+1/+1", "add", 2, "target creature you control")
        
        self.assertEqual(effect.counter_type, "+1/+1")
        self.assertEqual(effect.action, "add")
        self.assertEqual(effect.count, 2)
        self.assertEqual(effect.target, "target creature you control")
        self.assertEqual(effect.expression_type, MTGExpression.ExpressionType.COUNTER)
    
    def test_setters(self):
        """Test setting counter effect properties."""
        effect = CounterEffect("+1/+1", "add", 2, "target creature you control")
        effect.counter_type = "loyalty"
        effect.action = "remove"
        effect.count = 1
        effect.target = "this planeswalker"
        
        self.assertEqual(effect.counter_type, "loyalty")
        self.assertEqual(effect.action, "remove")
        self.assertEqual(effect.count, 1)
        self.assertEqual(effect.target, "this planeswalker")
    
    def test_to_dict(self):
        """Test converting a counter effect to a dictionary."""
        effect = CounterEffect("+1/+1", "add", 2, "target creature you control")
        
        effect_dict = effect.to_dict()
        self.assertEqual(effect_dict['type'], 'CounterEffect')
        self.assertEqual(effect_dict['counter_type'], "+1/+1")
        self.assertEqual(effect_dict['action'], "add")
        self.assertEqual(effect_dict['count'], 2)
        self.assertEqual(effect_dict['target'], "target creature you control")


class TestCostModification(unittest.TestCase):
    """Test cases for the CostModification class."""
    
    def test_initialization(self):
        """Test initializing a cost modification."""
        modification = CostModification("reduce", "{1}", "for each Cat you control", 
                                       "This spell costs {1} less to cast for each Cat you control.")
        
        self.assertEqual(modification.modification_type, "reduce")
        self.assertEqual(modification.cost, "{1}")
        self.assertEqual(modification.condition, "for each Cat you control")
        self.assertEqual(modification.reminder_text, "This spell costs {1} less to cast for each Cat you control.")
        self.assertEqual(modification.statement_type, MTGStatement.StatementType.COST_MODIFICATION)
    
    def test_setters(self):
        """Test setting cost modification properties."""
        modification = CostModification("reduce", "{1}", "for each Cat you control")
        modification.modification_type = "additional"
        modification.cost = "{2}{W}"
        modification.condition = None
        modification.reminder_text = "You may pay an additional {2}{W} as you cast this spell."
        
        self.assertEqual(modification.modification_type, "additional")
        self.assertEqual(modification.cost, "{2}{W}")
        self.assertIsNone(modification.condition)
        self.assertEqual(modification.reminder_text, "You may pay an additional {2}{W} as you cast this spell.")
    
    def test_to_dict(self):
        """Test converting a cost modification to a dictionary."""
        modification = CostModification("reduce", "{1}", "for each Cat you control", 
                                       "This spell costs {1} less to cast for each Cat you control.")
        
        modification_dict = modification.to_dict()
        self.assertEqual(modification_dict['type'], 'CostModification')
        self.assertEqual(modification_dict['modification_type'], "reduce")
        self.assertEqual(modification_dict['cost'], "{1}")
        self.assertEqual(modification_dict['condition'], "for each Cat you control")
        self.assertEqual(modification_dict['reminder_text'], "This spell costs {1} less to cast for each Cat you control.")


if __name__ == '__main__':
    unittest.main()