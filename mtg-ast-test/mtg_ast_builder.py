"""
Utility class for building Magic: The Gathering Abstract Syntax Trees (ASTs).

This module provides a builder class to simplify the construction of MTG ASTs.
"""
from typing import List, Optional, Dict, Any, Union, Tuple
from mtg_ast import MTGNode, MTGDeclaration, MTGStatement, MTGExpression
from mtg_ast_specialized import (
    KeywordAbility, TokenCreation, TriggeredAbility, StaticAbility,
    ConditionalEffect, TargetEffect, CounterEffect, CostModification,
    ActivatedAbility, ConditionalTriggeredAbility, SpellSequence, VariableCostModification
)
from mtg_card_root import MTGCardRoot


class MTGCardBuilder:
    """
    Builder class for constructing MTG card ASTs.
    
    This class provides methods to simplify the construction of MTG card ASTs
    by providing high-level methods for common card text constructs.
    """
    
    def __init__(self):
        """Initialize an MTG card builder."""
        self.root = MTGCardRoot(None)
    
    def add_keyword_ability(self, 
                           keyword: str, 
                           reminder_text: Optional[str] = None,
                           target: Optional[str] = None) -> KeywordAbility:
        """
        Add a keyword ability to the card.
        
        Args:
            keyword: The keyword ability (e.g., "Flying", "First strike").
            reminder_text: The reminder text for the keyword, if any.
            target: The target of the keyword ability, if any.
        
        Returns:
            The created keyword ability node.
        """
        ability = KeywordAbility(keyword, reminder_text, target)
        self.root.add_child(ability)
        return ability
    
    def add_token_creation(self, 
                          power: int, 
                          toughness: int,
                          colors: List[str],
                          types: List[str],
                          subtypes: List[str],
                          count: int = 1) -> TokenCreation:
        """
        Add a token creation to the card.
        
        Args:
            power: The power of the token.
            toughness: The toughness of the token.
            colors: The colors of the token.
            types: The types of the token (e.g., "creature", "artifact").
            subtypes: The subtypes of the token (e.g., "Cat", "Knight").
            count: The number of tokens to create.
        
        Returns:
            The created token creation node.
        """
        token = TokenCreation(power, toughness, colors, types, subtypes, count)
        self.root.add_child(token)
        return token
    
    def add_triggered_ability(self, 
                             trigger: str, 
                             effect: Optional[MTGExpression] = None) -> TriggeredAbility:
        """
        Add a triggered ability to the card.
        
        Args:
            trigger: The trigger condition for the ability.
            effect: The effect of the ability, if any.
        
        Returns:
            The created triggered ability node.
        """
        ability = TriggeredAbility(trigger, effect)
        self.root.add_child(ability)
        return ability
    
    def add_static_ability(self, 
                          effect: str, 
                          target: Optional[str] = None) -> StaticAbility:
        """
        Add a static ability to the card.
        
        Args:
            effect: The effect of the static ability.
            target: The target of the static ability, if any.
        
        Returns:
            The created static ability node.
        """
        ability = StaticAbility(effect, target)
        self.root.add_child(ability)
        return ability
    
    def add_conditional_effect(self, 
                              condition: str, 
                              effect: Optional[MTGExpression] = None,
                              else_effect: Optional[MTGExpression] = None) -> ConditionalEffect:
        """
        Add a conditional effect to the card.
        
        Args:
            condition: The condition for the effect.
            effect: The effect if the condition is met, if any.
            else_effect: The effect if the condition is not met, if any.
        
        Returns:
            The created conditional effect node.
        """
        conditional = ConditionalEffect(condition, effect, else_effect)
        self.root.add_child(conditional)
        return conditional
    
    def add_target_effect(self, 
                         effect: str, 
                         target_type: str,
                         target_restrictions: Optional[List[str]] = None,
                         duration: Optional[str] = None) -> TargetEffect:
        """
        Add a targeted effect to the card.
        
        Args:
            effect: The effect to apply to the target.
            target_type: The type of target (e.g., "creature", "player").
            target_restrictions: Restrictions on the target, if any.
            duration: The duration of the effect, if any.
        
        Returns:
            The created targeted effect node.
        """
        target_effect = TargetEffect(effect, target_type, target_restrictions, duration)
        self.root.add_child(target_effect)
        return target_effect
    
    def add_counter_effect(self, 
                          counter_type: str, 
                          action: str,
                          count: int = 1,
                          target: Optional[str] = None) -> CounterEffect:
        """
        Add a counter effect to the card.
        
        Args:
            counter_type: The type of counter (e.g., "+1/+1", "loyalty").
            action: The action to perform ("add" or "remove").
            count: The number of counters to add or remove.
            target: The target to add counters to or remove counters from, if any.
        
        Returns:
            The created counter effect node.
        """
        counter = CounterEffect(counter_type, action, count, target)
        self.root.add_child(counter)
        return counter
    
    def add_cost_modification(self, 
                             modification_type: str, 
                             cost: str,
                             condition: Optional[str] = None,
                             reminder_text: Optional[str] = None) -> CostModification:
        """
        Add a cost modification to the card.
        
        Args:
            modification_type: The type of cost modification.
            cost: The cost modification.
            condition: The condition for the cost modification, if any.
            reminder_text: The reminder text for the cost modification, if any.
        
        Returns:
            The created cost modification node.
        """
        modification = CostModification(modification_type, cost, condition, reminder_text)
        self.root.add_child(modification)
        return modification
    
    def add_activated_ability(self, 
                             cost: str, 
                             effect: str) -> ActivatedAbility:
        """
        Add an activated ability to the card.
        
        Args:
            cost: The cost to activate the ability.
            effect: The effect of the ability.
        
        Returns:
            The created activated ability node.
        """
        ability = ActivatedAbility(cost, effect)
        self.root.add_child(ability)
        return ability
    
    def add_conditional_triggered_ability(self, 
                                         trigger: str, 
                                         condition: str,
                                         effect: Optional[MTGExpression] = None) -> ConditionalTriggeredAbility:
        """
        Add a conditional triggered ability to the card.
        
        Args:
            trigger: The trigger condition for the ability.
            condition: The additional condition that must be met.
            effect: The effect of the ability, if any.
        
        Returns:
            The created conditional triggered ability node.
        """
        ability = ConditionalTriggeredAbility(trigger, condition, effect)
        self.root.add_child(ability)
        return ability
    
    def add_spell_sequence(self, 
                          effects: List[Dict[str, Any]]) -> SpellSequence:
        """
        Add a spell sequence to the card.
        
        Args:
            effects: A list of effect dictionaries describing the sequence.
        
        Returns:
            The created spell sequence node.
        """
        sequence = SpellSequence(effects)
        self.root.add_child(sequence)
        return sequence
    
    def add_variable_cost_modification(self, 
                                      modification_type: str, 
                                      cost: str,
                                      variable_definition: str,
                                      condition: Optional[str] = None,
                                      reminder_text: Optional[str] = None) -> VariableCostModification:
        """
        Add a variable cost modification to the card.
        
        Args:
            modification_type: The type of cost modification.
            cost: The cost modification (e.g., "{X}").
            variable_definition: The definition of the variable (e.g., "where X is...").
            condition: The condition for the cost modification, if any.
            reminder_text: The reminder text for the cost modification, if any.
        
        Returns:
            The created variable cost modification node.
        """
        modification = VariableCostModification(modification_type, cost, variable_definition, condition, reminder_text)
        self.root.add_child(modification)
        return modification
    
    def build(self) -> MTGNode:
        """
        Build the MTG card AST.
        
        Returns:
            The root node of the MTG card AST.
        """
        return self.root
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the MTG card AST to a dictionary representation.
        
        Returns:
            A dictionary representation of the MTG card AST.
        """
        return {
            'type': 'MTGCard',
            'children': [child.to_dict() for child in self.root.children]
        }
    
    def __str__(self) -> str:
        """Return a string representation of the MTG card AST."""
        return f"MTGCardBuilder({len(self.root.children)} nodes)"