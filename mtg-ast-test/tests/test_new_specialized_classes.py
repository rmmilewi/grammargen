"""
Unit tests for the new specialized MTG AST classes.
"""
import sys
import os
import unittest
from typing import List, Optional, Dict, Any

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtg_ast import MTGNode, MTGDeclaration, MTGStatement, MTGExpression
from mtg_ast_specialized import (
    ActivatedAbility, ConditionalTriggeredAbility, SpellSequence, VariableCostModification
)


class TestActivatedAbility(unittest.TestCase):
    """Test cases for the ActivatedAbility class."""
    
    def test_initialization(self):
        """Test initializing an activated ability."""
        ability = ActivatedAbility("{T}", "Add {G} for each Elf you control")
        
        self.assertEqual(ability.cost, "{T}")
        self.assertEqual(ability.effect, "Add {G} for each Elf you control")
        self.assertEqual(ability.statement_type, MTGStatement.StatementType.ACTIVATED_ABILITY)
    
    def test_setters(self):
        """Test setting activated ability properties."""
        ability = ActivatedAbility("{T}", "Add {G} for each Elf you control")
        ability.cost = "{2}, {T}"
        ability.effect = "Draw a card"
        
        self.assertEqual(ability.cost, "{2}, {T}")
        self.assertEqual(ability.effect, "Draw a card")
    
    def test_to_dict(self):
        """Test converting an activated ability to a dictionary."""
        ability = ActivatedAbility("{T}", "Add {G} for each Elf you control")
        
        ability_dict = ability.to_dict()
        self.assertEqual(ability_dict['type'], 'ActivatedAbility')
        self.assertEqual(ability_dict['cost'], '{T}')
        self.assertEqual(ability_dict['effect'], 'Add {G} for each Elf you control')


class TestConditionalTriggeredAbility(unittest.TestCase):
    """Test cases for the ConditionalTriggeredAbility class."""
    
    def test_initialization(self):
        """Test initializing a conditional triggered ability."""
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
        ability = ConditionalTriggeredAbility("when this enchantment enters", 
                                             "if you control a creature with power 4 or greater", 
                                             effect)
        
        self.assertEqual(ability.trigger, "when this enchantment enters")
        self.assertEqual(ability.condition, "if you control a creature with power 4 or greater")
        self.assertEqual(ability.effect, effect)
        self.assertEqual(ability.statement_type, MTGStatement.StatementType.TRIGGERED_ABILITY)
    
    def test_initialization_without_effect(self):
        """Test initializing a conditional triggered ability without an effect."""
        ability = ConditionalTriggeredAbility("when this enchantment enters", 
                                             "if you control a creature with power 4 or greater")
        
        self.assertEqual(ability.trigger, "when this enchantment enters")
        self.assertEqual(ability.condition, "if you control a creature with power 4 or greater")
        self.assertIsNone(ability.effect)
    
    def test_set_effect(self):
        """Test setting the effect of a conditional triggered ability."""
        ability = ConditionalTriggeredAbility("when this enchantment enters", 
                                             "if you control a creature with power 4 or greater")
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
        ability.set_effect(effect)
        
        self.assertEqual(ability.effect, effect)
        self.assertIn(effect, ability.children)
    
    def test_to_dict(self):
        """Test converting a conditional triggered ability to a dictionary."""
        effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
        ability = ConditionalTriggeredAbility("when this enchantment enters", 
                                             "if you control a creature with power 4 or greater", 
                                             effect)
        
        ability_dict = ability.to_dict()
        self.assertEqual(ability_dict['type'], 'ConditionalTriggeredAbility')
        self.assertEqual(ability_dict['trigger'], "when this enchantment enters")
        self.assertEqual(ability_dict['condition'], "if you control a creature with power 4 or greater")
        self.assertEqual(len(ability_dict['children']), 1)


class TestSpellSequence(unittest.TestCase):
    """Test cases for the SpellSequence class."""
    
    def test_initialization(self):
        """Test initializing a spell sequence."""
        effects = [
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
            }
        ]
        sequence = SpellSequence(effects)
        
        self.assertEqual(len(sequence.effects), 2)
        self.assertEqual(sequence.effects[0]["type"], "reveal")
        self.assertEqual(sequence.effects[1]["type"], "optional_put")
    
    def test_add_effect(self):
        """Test adding an effect to a spell sequence."""
        effects = [
            {
                "type": "reveal",
                "target": "top X cards of your library",
                "zone": "library"
            }
        ]
        sequence = SpellSequence(effects)
        
        new_effect = {
            "type": "put",
            "source": "remaining revealed cards",
            "target": "graveyard"
        }
        sequence.add_effect(new_effect)
        
        self.assertEqual(len(sequence.effects), 2)
        self.assertEqual(sequence.effects[1]["type"], "put")
    
    def test_to_dict(self):
        """Test converting a spell sequence to a dictionary."""
        effects = [
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
            }
        ]
        sequence = SpellSequence(effects)
        
        sequence_dict = sequence.to_dict()
        self.assertEqual(sequence_dict['type'], 'SpellSequence')
        self.assertEqual(len(sequence_dict['effects']), 2)
        self.assertEqual(sequence_dict['effects'][0]['type'], 'reveal')
        self.assertEqual(sequence_dict['effects'][1]['type'], 'optional_put')


class TestVariableCostModification(unittest.TestCase):
    """Test cases for the VariableCostModification class."""
    
    def test_initialization(self):
        """Test initializing a variable cost modification."""
        modification = VariableCostModification("reduce", "{X}", 
                                               "where X is the total power of creatures you control")
        
        self.assertEqual(modification.modification_type, "reduce")
        self.assertEqual(modification.cost, "{X}")
        self.assertEqual(modification.variable_definition, "where X is the total power of creatures you control")
        self.assertEqual(modification.statement_type, MTGStatement.StatementType.COST_MODIFICATION)
    
    def test_setters(self):
        """Test setting variable cost modification properties."""
        modification = VariableCostModification("reduce", "{X}", 
                                               "where X is the total power of creatures you control")
        modification.modification_type = "increase"
        modification.cost = "{Y}"
        modification.variable_definition = "where Y is the number of artifacts you control"
        modification.reminder_text = "This spell costs {Y} more to cast"
        
        self.assertEqual(modification.modification_type, "increase")
        self.assertEqual(modification.cost, "{Y}")
        self.assertEqual(modification.variable_definition, "where Y is the number of artifacts you control")
        self.assertEqual(modification.reminder_text, "This spell costs {Y} more to cast")
    
    def test_to_dict(self):
        """Test converting a variable cost modification to a dictionary."""
        modification = VariableCostModification("reduce", "{X}", 
                                               "where X is the total power of creatures you control",
                                               None, "This spell costs {X} less to cast")
        
        modification_dict = modification.to_dict()
        self.assertEqual(modification_dict['type'], 'VariableCostModification')
        self.assertEqual(modification_dict['modification_type'], "reduce")
        self.assertEqual(modification_dict['cost'], "{X}")
        self.assertEqual(modification_dict['variable_definition'], "where X is the total power of creatures you control")
        self.assertEqual(modification_dict['reminder_text'], "This spell costs {X} less to cast")


if __name__ == '__main__':
    unittest.main()