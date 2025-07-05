"""
Test-driven development tests for new MTG card examples.

This module contains tests for building ASTs for specific MTG cards,
driving the development of new AST node types and functionality.
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


class TestNewCardExamples(unittest.TestCase):
    """Test cases for new MTG card examples that drive AST development."""
    
    def test_elf_lord_with_activated_ability(self):
        """
        Test constructing an Elf lord card with static and activated abilities.
        
        Card text: "Other Elf creatures you control get +1/+1.
        {T}: Add {G} for each Elf you control."
        """
        builder = MTGCardBuilder()
        
        # Static ability: "Other Elf creatures you control get +1/+1."
        builder.add_static_ability("get +1/+1", "other Elf creatures you control")
        
        # Activated ability: "{T}: Add {G} for each Elf you control."
        # This requires a new ActivatedAbility class
        activated_ability = builder.add_activated_ability(
            cost="{T}",
            effect="Add {G} for each Elf you control"
        )
        
        card = builder.build()
        self.assertEqual(len(card.children), 2)
        
        # Check static ability
        static_ability = card.children[0]
        self.assertIsInstance(static_ability, StaticAbility)
        self.assertEqual(static_ability.effect, "get +1/+1")
        self.assertEqual(static_ability.target, "other Elf creatures you control")
        
        # Check activated ability
        activated = card.children[1]
        self.assertEqual(activated.cost, "{T}")
        self.assertEqual(activated.effect, "Add {G} for each Elf you control")
    
    def test_enchantment_with_conditional_trigger(self):
        """
        Test constructing an enchantment with conditional triggered abilities.
        
        Card text: "When this enchantment enters, if you control a creature with power 4 or greater, draw 1 card.
        Creatures you control have trample. (Each of those creatures can deal excess combat damage to the player or planeswalker it's attacking.)
        Whenever a creature you control with power 4 or greater enters, draw 1 card."
        """
        builder = MTGCardBuilder()
        
        # Conditional triggered ability: "When this enchantment enters, if you control a creature with power 4 or greater, draw 1 card."
        trigger1 = "when this enchantment enters"
        condition1 = "if you control a creature with power 4 or greater"
        effect1 = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
        
        conditional_trigger = builder.add_conditional_triggered_ability(
            trigger=trigger1,
            condition=condition1,
            effect=effect1
        )
        
        # Static ability with reminder text: "Creatures you control have trample."
        builder.add_keyword_ability("Trample", 
                                   "Each of those creatures can deal excess combat damage to the player or planeswalker it's attacking.",
                                   target="creatures you control")
        
        # Regular triggered ability: "Whenever a creature you control with power 4 or greater enters, draw 1 card."
        trigger2 = "whenever a creature you control with power 4 or greater enters"
        effect2 = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
        builder.add_triggered_ability(trigger2, effect2)
        
        card = builder.build()
        self.assertEqual(len(card.children), 3)
        
        # Check conditional triggered ability
        conditional = card.children[0]
        self.assertEqual(conditional.trigger, trigger1)
        self.assertEqual(conditional.condition, condition1)
        
        # Check keyword ability with target
        keyword = card.children[1]
        self.assertIsInstance(keyword, KeywordAbility)
        self.assertEqual(keyword.keyword, "Trample")
        self.assertEqual(keyword.target, "creatures you control")
        
        # Check regular triggered ability
        triggered = card.children[2]
        self.assertIsInstance(triggered, TriggeredAbility)
        self.assertEqual(triggered.trigger, trigger2)
    
    def test_spell_with_sequential_effects(self):
        """
        Test constructing a spell with sequential effects.
        
        Card text: "Reveal the top X cards of your library. You may put any number of permanent cards with mana value X or less from among them onto the battlefield. Then put all cards revealed this way that weren't put onto the battlefield into your graveyard."
        """
        builder = MTGCardBuilder()
        
        # This spell has sequential effects that need to be represented as a sequence
        spell_effects = builder.add_spell_sequence([
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
        
        card = builder.build()
        self.assertEqual(len(card.children), 1)
        
        # Check spell sequence
        sequence = card.children[0]
        self.assertEqual(len(sequence.effects), 3)
        
        # Check individual effects
        reveal_effect = sequence.effects[0]
        self.assertEqual(reveal_effect["type"], "reveal")
        self.assertEqual(reveal_effect["target"], "top X cards of your library")
        
        put_effect = sequence.effects[1]
        self.assertEqual(put_effect["type"], "optional_put")
        self.assertEqual(put_effect["restriction"], "permanent cards with mana value X or less")
        
        graveyard_effect = sequence.effects[2]
        self.assertEqual(graveyard_effect["type"], "put")
        self.assertEqual(graveyard_effect["target"], "graveyard")
    
    def test_spell_with_variable_cost_reduction(self):
        """
        Test constructing a spell with variable cost reduction.
        
        Card text: "This spell costs {X} less to cast, where X is the total power of creatures you control.
        Trample (Reminder text)"
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
        
        card = builder.build()
        self.assertEqual(len(card.children), 2)
        
        # Check variable cost modification
        cost_mod = card.children[0]
        self.assertEqual(cost_mod.modification_type, "reduce")
        self.assertEqual(cost_mod.cost, "{X}")
        self.assertEqual(cost_mod.variable_definition, "where X is the total power of creatures you control")
        
        # Check keyword ability
        keyword = card.children[1]
        self.assertIsInstance(keyword, KeywordAbility)
        self.assertEqual(keyword.keyword, "Trample")
        self.assertEqual(keyword.reminder_text, "Reminder text")


if __name__ == '__main__':
    unittest.main()