"""
Specialized Magic: The Gathering Abstract Syntax Tree (AST) nodes.

This module defines specialized node classes that extend the base MTG AST classes
to handle specific MTG card text constructs.
"""
from typing import List, Optional, Dict, Any, Union, Tuple
from mtg_ast import MTGNode, MTGDeclaration, MTGStatement, MTGExpression


class KeywordAbility(MTGDeclaration):
    """
    Represents a keyword ability in MTG card text.
    
    Examples:
    - "Flying"
    - "First strike"
    - "Vigilance"
    - "Creatures you control have trample"
    """
    
    def __init__(self, 
                 keyword: str, 
                 reminder_text: Optional[str] = None,
                 target: Optional[str] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a keyword ability node.
        
        Args:
            keyword: The keyword ability (e.g., "Flying", "First strike").
            reminder_text: The reminder text for the keyword, if any.
            target: The target of the keyword ability, if any (e.g., "creatures you control").
            parent: The parent node in the AST, if any.
        """
        super().__init__("keyword_ability", keyword, parent)
        self._reminder_text = reminder_text
        self._target = target
    
    @property
    def keyword(self) -> str:
        """Get the keyword ability."""
        return self.value
    
    @keyword.setter
    def keyword(self, keyword: str):
        """Set the keyword ability."""
        self.value = keyword
    
    @property
    def reminder_text(self) -> Optional[str]:
        """Get the reminder text."""
        return self._reminder_text
    
    @reminder_text.setter
    def reminder_text(self, reminder_text: Optional[str]):
        """Set the reminder text."""
        self._reminder_text = reminder_text
    
    @property
    def target(self) -> Optional[str]:
        """Get the target of the keyword ability."""
        return self._target
    
    @target.setter
    def target(self, target: Optional[str]):
        """Set the target of the keyword ability."""
        self._target = target
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the keyword ability to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'keyword': self.value,
            'reminder_text': self._reminder_text,
            'target': self._target
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the keyword ability."""
        parts = [self.value]
        if self._reminder_text:
            parts.append(f"reminder={self._reminder_text}")
        if self._target:
            parts.append(f"target={self._target}")
        return f"{self.__class__.__name__}({', '.join(parts)})"


class TokenCreation(MTGDeclaration):
    """
    Represents a token creation in MTG card text.
    
    Examples:
    - "Create a 1/1 white Cat creature token."
    - "Create two 3/3 white Knight creature tokens."
    """
    
    def __init__(self, 
                 power: int, 
                 toughness: int,
                 colors: List[str],
                 types: List[str],
                 subtypes: List[str],
                 count: int = 1,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a token creation node.
        
        Args:
            power: The power of the token.
            toughness: The toughness of the token.
            colors: The colors of the token.
            types: The types of the token (e.g., "creature", "artifact").
            subtypes: The subtypes of the token (e.g., "Cat", "Knight").
            count: The number of tokens to create.
            parent: The parent node in the AST, if any.
        """
        token_value = {
            'power': power,
            'toughness': toughness,
            'colors': colors,
            'types': types,
            'subtypes': subtypes,
            'count': count
        }
        super().__init__("token_creation", token_value, parent)
    
    @property
    def power(self) -> int:
        """Get the token power."""
        return self.value['power']
    
    @power.setter
    def power(self, power: int):
        """Set the token power."""
        self.value['power'] = power
    
    @property
    def toughness(self) -> int:
        """Get the token toughness."""
        return self.value['toughness']
    
    @toughness.setter
    def toughness(self, toughness: int):
        """Set the token toughness."""
        self.value['toughness'] = toughness
    
    @property
    def colors(self) -> List[str]:
        """Get the token colors."""
        return self.value['colors']
    
    @colors.setter
    def colors(self, colors: List[str]):
        """Set the token colors."""
        self.value['colors'] = colors
    
    @property
    def types(self) -> List[str]:
        """Get the token types."""
        return self.value['types']
    
    @types.setter
    def types(self, types: List[str]):
        """Set the token types."""
        self.value['types'] = types
    
    @property
    def subtypes(self) -> List[str]:
        """Get the token subtypes."""
        return self.value['subtypes']
    
    @subtypes.setter
    def subtypes(self, subtypes: List[str]):
        """Set the token subtypes."""
        self.value['subtypes'] = subtypes
    
    @property
    def count(self) -> int:
        """Get the token count."""
        return self.value['count']
    
    @count.setter
    def count(self, count: int):
        """Set the token count."""
        self.value['count'] = count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the token creation to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'power': self.power,
            'toughness': self.toughness,
            'colors': self.colors,
            'types': self.types,
            'subtypes': self.subtypes,
            'count': self.count
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the token creation."""
        return (f"{self.__class__.__name__}({self.count} {'/'.join(self.colors)} "
                f"{self.power}/{self.toughness} {', '.join(self.subtypes)} {', '.join(self.types)})")


class TriggeredAbility(MTGStatement):
    """
    Represents a triggered ability in MTG card text.
    
    Examples:
    - "When this creature enters the battlefield, draw a card."
    - "Whenever you gain life, put a +1/+1 counter on this creature."
    """
    
    def __init__(self, 
                 trigger: str, 
                 effect: Optional[MTGExpression] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a triggered ability node.
        
        Args:
            trigger: The trigger condition for the ability.
            effect: The effect of the ability, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(self.StatementType.TRIGGERED_ABILITY, trigger, parent)
        if effect:
            self.add_child(effect)
    
    @property
    def trigger(self) -> str:
        """Get the trigger condition."""
        return self.condition
    
    @trigger.setter
    def trigger(self, trigger: str):
        """Set the trigger condition."""
        self.condition = trigger
    
    @property
    def effect(self) -> Optional[MTGExpression]:
        """Get the effect of the triggered ability."""
        for child in self.children:
            if isinstance(child, MTGExpression):
                return child
        return None
    
    def set_effect(self, effect: MTGExpression):
        """
        Set the effect of the triggered ability.
        
        Args:
            effect: The effect to set.
        """
        current_effect = self.effect
        if current_effect:
            self.remove_child(current_effect)
        self.add_child(effect)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the triggered ability to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'trigger': self.trigger
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the triggered ability."""
        effect_str = f", {self.effect}" if self.effect else ""
        return f"{self.__class__.__name__}({self.trigger}{effect_str})"


class StaticAbility(MTGStatement):
    """
    Represents a static ability in MTG card text.
    
    Examples:
    - "You have hexproof."
    - "Creatures you control get +1/+1."
    """
    
    def __init__(self, 
                 effect: str, 
                 target: Optional[str] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a static ability node.
        
        Args:
            effect: The effect of the static ability.
            target: The target of the static ability, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(self.StatementType.STATIC_ABILITY, None, parent)
        effect_expr = MTGExpression(MTGExpression.ExpressionType.EFFECT, effect, target)
        self.add_child(effect_expr)
    
    @property
    def effect(self) -> str:
        """Get the effect of the static ability."""
        effect_expr = self.effect_expression
        return effect_expr.value if effect_expr else ""
    
    @effect.setter
    def effect(self, effect: str):
        """Set the effect of the static ability."""
        effect_expr = self.effect_expression
        if effect_expr:
            effect_expr.value = effect
        else:
            self.add_child(MTGExpression(MTGExpression.ExpressionType.EFFECT, effect))
    
    @property
    def target(self) -> Optional[str]:
        """Get the target of the static ability."""
        effect_expr = self.effect_expression
        return effect_expr.target if effect_expr else None
    
    @target.setter
    def target(self, target: Optional[str]):
        """Set the target of the static ability."""
        effect_expr = self.effect_expression
        if effect_expr:
            effect_expr.target = target
    
    @property
    def effect_expression(self) -> Optional[MTGExpression]:
        """Get the effect expression of the static ability."""
        for child in self.children:
            if isinstance(child, MTGExpression) and child.expression_type == MTGExpression.ExpressionType.EFFECT:
                return child
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the static ability to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'effect': self.effect,
            'target': self.target
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the static ability."""
        target_str = f", target={self.target}" if self.target else ""
        return f"{self.__class__.__name__}({self.effect}{target_str})"


class ConditionalEffect(MTGStatement):
    """
    Represents a conditional effect in MTG card text.
    
    Examples:
    - "If this spell was kicked, instead any number of target creatures you control gain indestructible until end of turn."
    - "If you control three or more creatures, draw a card."
    """
    
    def __init__(self, 
                 condition: str, 
                 effect: Optional[MTGExpression] = None,
                 else_effect: Optional[MTGExpression] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a conditional effect node.
        
        Args:
            condition: The condition for the effect.
            effect: The effect if the condition is met, if any.
            else_effect: The effect if the condition is not met, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(self.StatementType.CONDITIONAL, condition, parent)
        if effect:
            self.add_child(effect)
        if else_effect:
            self.add_child(else_effect)
            else_effect._is_else = True  # Mark as else effect
    
    @property
    def effect(self) -> Optional[MTGExpression]:
        """Get the effect if the condition is met."""
        for child in self.children:
            if isinstance(child, MTGExpression) and not getattr(child, '_is_else', False):
                return child
        return None
    
    def set_effect(self, effect: MTGExpression):
        """
        Set the effect if the condition is met.
        
        Args:
            effect: The effect to set.
        """
        current_effect = self.effect
        if current_effect:
            self.remove_child(current_effect)
        self.add_child(effect)
    
    @property
    def else_effect(self) -> Optional[MTGExpression]:
        """Get the effect if the condition is not met."""
        for child in self.children:
            if isinstance(child, MTGExpression) and getattr(child, '_is_else', False):
                return child
        return None
    
    def set_else_effect(self, else_effect: MTGExpression):
        """
        Set the effect if the condition is not met.
        
        Args:
            else_effect: The effect to set.
        """
        current_else_effect = self.else_effect
        if current_else_effect:
            self.remove_child(current_else_effect)
        self.add_child(else_effect)
        else_effect._is_else = True  # Mark as else effect
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the conditional effect to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'condition': self.condition,
            'has_else': self.else_effect is not None
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the conditional effect."""
        effect_str = f", {self.effect}" if self.effect else ""
        else_str = f", else={self.else_effect}" if self.else_effect else ""
        return f"{self.__class__.__name__}({self.condition}{effect_str}{else_str})"


class TargetEffect(MTGExpression):
    """
    Represents a targeted effect in MTG card text.
    
    Examples:
    - "Target creature gets +2/+2 until end of turn."
    - "Target player draws a card."
    """
    
    def __init__(self, 
                 effect: str, 
                 target_type: str,
                 target_restrictions: Optional[List[str]] = None,
                 duration: Optional[str] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a targeted effect node.
        
        Args:
            effect: The effect to apply to the target.
            target_type: The type of target (e.g., "creature", "player").
            target_restrictions: Restrictions on the target, if any.
            duration: The duration of the effect, if any.
            parent: The parent node in the AST, if any.
        """
        target_desc = target_type
        if target_restrictions:
            target_desc += " " + " ".join(target_restrictions)
        
        super().__init__(self.ExpressionType.EFFECT, effect, target_desc, parent)
        self._target_type = target_type
        self._target_restrictions = target_restrictions or []
        self._duration = duration
        
        if duration:
            duration_expr = MTGExpression(self.ExpressionType.DURATION, duration)
            self.add_child(duration_expr)
    
    @property
    def target_type(self) -> str:
        """Get the target type."""
        return self._target_type
    
    @target_type.setter
    def target_type(self, target_type: str):
        """Set the target type."""
        self._target_type = target_type
        self._update_target()
    
    @property
    def target_restrictions(self) -> List[str]:
        """Get the target restrictions."""
        return self._target_restrictions.copy()
    
    @target_restrictions.setter
    def target_restrictions(self, target_restrictions: List[str]):
        """Set the target restrictions."""
        self._target_restrictions = target_restrictions
        self._update_target()
    
    def _update_target(self):
        """Update the target description based on type and restrictions."""
        target_desc = self._target_type
        if self._target_restrictions:
            target_desc += " " + " ".join(self._target_restrictions)
        self.target = target_desc
    
    @property
    def duration(self) -> Optional[str]:
        """Get the duration of the effect."""
        return self._duration
    
    @duration.setter
    def duration(self, duration: Optional[str]):
        """Set the duration of the effect."""
        self._duration = duration
        
        # Remove existing duration expression
        for child in self.children:
            if isinstance(child, MTGExpression) and child.expression_type == self.ExpressionType.DURATION:
                self.remove_child(child)
        
        # Add new duration expression if needed
        if duration:
            duration_expr = MTGExpression(self.ExpressionType.DURATION, duration)
            self.add_child(duration_expr)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the targeted effect to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'target_type': self._target_type,
            'target_restrictions': self._target_restrictions,
            'duration': self._duration
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the targeted effect."""
        parts = [f"effect={self.value}", f"target_type={self._target_type}"]
        if self._target_restrictions:
            parts.append(f"restrictions={self._target_restrictions}")
        if self._duration:
            parts.append(f"duration={self._duration}")
        return f"{self.__class__.__name__}({', '.join(parts)})"


class CounterEffect(MTGExpression):
    """
    Represents a counter effect in MTG card text.
    
    Examples:
    - "Put a +1/+1 counter on target creature."
    - "Remove a loyalty counter from this planeswalker."
    """
    
    def __init__(self, 
                 counter_type: str, 
                 action: str,  # "add" or "remove"
                 count: int = 1,
                 target: Optional[str] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a counter effect node.
        
        Args:
            counter_type: The type of counter (e.g., "+1/+1", "loyalty").
            action: The action to perform ("add" or "remove").
            count: The number of counters to add or remove.
            target: The target to add counters to or remove counters from, if any.
            parent: The parent node in the AST, if any.
        """
        counter_value = {
            'counter_type': counter_type,
            'action': action,
            'count': count
        }
        super().__init__(self.ExpressionType.COUNTER, counter_value, target, parent)
    
    @property
    def counter_type(self) -> str:
        """Get the counter type."""
        return self.value['counter_type']
    
    @counter_type.setter
    def counter_type(self, counter_type: str):
        """Set the counter type."""
        self.value['counter_type'] = counter_type
    
    @property
    def action(self) -> str:
        """Get the counter action."""
        return self.value['action']
    
    @action.setter
    def action(self, action: str):
        """Set the counter action."""
        self.value['action'] = action
    
    @property
    def count(self) -> int:
        """Get the counter count."""
        return self.value['count']
    
    @count.setter
    def count(self, count: int):
        """Set the counter count."""
        self.value['count'] = count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the counter effect to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'counter_type': self.counter_type,
            'action': self.action,
            'count': self.count
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the counter effect."""
        target_str = f", target={self.target}" if self.target else ""
        return f"{self.__class__.__name__}({self.action} {self.count} {self.counter_type}{target_str})"


class CostModification(MTGStatement):
    """
    Represents a cost modification in MTG card text.
    
    Examples:
    - "This spell costs {1} less to cast for each Cat you control."
    - "Kicker {2}{W} (You may pay an additional {2}{W} as you cast this spell.)"
    """
    
    def __init__(self, 
                 modification_type: str,  # "reduce", "increase", "alternative", "additional"
                 cost: str,
                 condition: Optional[str] = None,
                 reminder_text: Optional[str] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a cost modification node.
        
        Args:
            modification_type: The type of cost modification.
            cost: The cost modification.
            condition: The condition for the cost modification, if any.
            reminder_text: The reminder text for the cost modification, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(self.StatementType.COST_MODIFICATION, condition, parent)
        self._modification_type = modification_type
        self._cost = cost
        self._reminder_text = reminder_text
    
    @property
    def modification_type(self) -> str:
        """Get the modification type."""
        return self._modification_type
    
    @modification_type.setter
    def modification_type(self, modification_type: str):
        """Set the modification type."""
        self._modification_type = modification_type
    
    @property
    def cost(self) -> str:
        """Get the cost modification."""
        return self._cost
    
    @cost.setter
    def cost(self, cost: str):
        """Set the cost modification."""
        self._cost = cost
    
    @property
    def reminder_text(self) -> Optional[str]:
        """Get the reminder text."""
        return self._reminder_text
    
    @reminder_text.setter
    def reminder_text(self, reminder_text: Optional[str]):
        """Set the reminder text."""
        self._reminder_text = reminder_text
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the cost modification to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'modification_type': self._modification_type,
            'cost': self._cost,
            'reminder_text': self._reminder_text
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the cost modification."""
        condition_str = f", condition={self.condition}" if self.condition else ""
        reminder_str = f", reminder={self._reminder_text}" if self._reminder_text else ""
        return f"{self.__class__.__name__}({self._modification_type}, {self._cost}{condition_str}{reminder_str})"


class ActivatedAbility(MTGStatement):
    """
    Represents an activated ability in MTG card text.
    
    Examples:
    - "{T}: Add {G} for each Elf you control."
    - "{2}, {T}: Draw a card."
    """
    
    def __init__(self, 
                 cost: str, 
                 effect: str,
                 parent: Optional[MTGNode] = None):
        """
        Initialize an activated ability node.
        
        Args:
            cost: The cost to activate the ability.
            effect: The effect of the ability.
            parent: The parent node in the AST, if any.
        """
        super().__init__(self.StatementType.ACTIVATED_ABILITY, None, parent)
        self._cost = cost
        self._effect = effect
    
    @property
    def cost(self) -> str:
        """Get the activation cost."""
        return self._cost
    
    @cost.setter
    def cost(self, cost: str):
        """Set the activation cost."""
        self._cost = cost
    
    @property
    def effect(self) -> str:
        """Get the effect of the activated ability."""
        return self._effect
    
    @effect.setter
    def effect(self, effect: str):
        """Set the effect of the activated ability."""
        self._effect = effect
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the activated ability to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'cost': self._cost,
            'effect': self._effect
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the activated ability."""
        return f"{self.__class__.__name__}({self._cost}: {self._effect})"


class ConditionalTriggeredAbility(MTGStatement):
    """
    Represents a triggered ability with an additional condition.
    
    Examples:
    - "When this enchantment enters, if you control a creature with power 4 or greater, draw 1 card."
    """
    
    def __init__(self, 
                 trigger: str, 
                 condition: str,
                 effect: Optional[MTGExpression] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a conditional triggered ability node.
        
        Args:
            trigger: The trigger condition for the ability.
            condition: The additional condition that must be met.
            effect: The effect of the ability, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(self.StatementType.TRIGGERED_ABILITY, condition, parent)
        self._trigger = trigger
        if effect:
            self.add_child(effect)
    
    @property
    def trigger(self) -> str:
        """Get the trigger condition."""
        return self._trigger
    
    @trigger.setter
    def trigger(self, trigger: str):
        """Set the trigger condition."""
        self._trigger = trigger
    
    @property
    def effect(self) -> Optional[MTGExpression]:
        """Get the effect of the conditional triggered ability."""
        for child in self.children:
            if isinstance(child, MTGExpression):
                return child
        return None
    
    def set_effect(self, effect: MTGExpression):
        """
        Set the effect of the conditional triggered ability.
        
        Args:
            effect: The effect to set.
        """
        current_effect = self.effect
        if current_effect:
            self.remove_child(current_effect)
        self.add_child(effect)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the conditional triggered ability to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'trigger': self._trigger
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the conditional triggered ability."""
        effect_str = f", {self.effect}" if self.effect else ""
        return f"{self.__class__.__name__}({self._trigger}, {self.condition}{effect_str})"


class SpellSequence(MTGStatement):
    """
    Represents a sequence of spell effects that happen in order.
    
    Examples:
    - "Reveal the top X cards of your library. You may put any number of permanent cards with mana value X or less from among them onto the battlefield. Then put all cards revealed this way that weren't put onto the battlefield into your graveyard."
    """
    
    def __init__(self, 
                 effects: List[Dict[str, Any]],
                 parent: Optional[MTGNode] = None):
        """
        Initialize a spell sequence node.
        
        Args:
            effects: A list of effect dictionaries describing the sequence.
            parent: The parent node in the AST, if any.
        """
        super().__init__("spell_sequence", None, parent)
        self._effects = effects
    
    @property
    def effects(self) -> List[Dict[str, Any]]:
        """Get the list of effects in the sequence."""
        return self._effects.copy()
    
    @effects.setter
    def effects(self, effects: List[Dict[str, Any]]):
        """Set the list of effects in the sequence."""
        self._effects = effects
    
    def add_effect(self, effect: Dict[str, Any]):
        """
        Add an effect to the sequence.
        
        Args:
            effect: The effect dictionary to add.
        """
        self._effects.append(effect)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the spell sequence to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'effects': self._effects
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the spell sequence."""
        return f"{self.__class__.__name__}({len(self._effects)} effects)"


class VariableCostModification(CostModification):
    """
    Represents a cost modification with a variable component.
    
    Examples:
    - "This spell costs {X} less to cast, where X is the total power of creatures you control."
    """
    
    def __init__(self, 
                 modification_type: str,
                 cost: str,
                 variable_definition: str,
                 condition: Optional[str] = None,
                 reminder_text: Optional[str] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize a variable cost modification node.
        
        Args:
            modification_type: The type of cost modification.
            cost: The cost modification (e.g., "{X}").
            variable_definition: The definition of the variable (e.g., "where X is...").
            condition: The condition for the cost modification, if any.
            reminder_text: The reminder text for the cost modification, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(modification_type, cost, condition, reminder_text, parent)
        self._variable_definition = variable_definition
    
    @property
    def variable_definition(self) -> str:
        """Get the variable definition."""
        return self._variable_definition
    
    @variable_definition.setter
    def variable_definition(self, variable_definition: str):
        """Set the variable definition."""
        self._variable_definition = variable_definition
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the variable cost modification to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'variable_definition': self._variable_definition
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the variable cost modification."""
        condition_str = f", condition={self.condition}" if self.condition else ""
        reminder_str = f", reminder={self.reminder_text}" if self.reminder_text else ""
        return f"{self.__class__.__name__}({self.modification_type}, {self.cost}, {self._variable_definition}{condition_str}{reminder_str})"