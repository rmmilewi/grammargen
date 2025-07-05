"""
Magic: The Gathering Abstract Syntax Tree (AST) implementation.

This module defines a class hierarchy for representing Magic: The Gathering card text
in a structured, parseable form similar to how compilers represent source code.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class MTGNode(ABC):
    """
    Abstract base class for all MTG AST nodes.
    
    All nodes in the MTG AST inherit from this class, providing a common
    interface for traversal and manipulation.
    """
    
    def __init__(self, parent: Optional['MTGNode'] = None):
        """
        Initialize an MTG AST node.
        
        Args:
            parent: The parent node in the AST, if any.
        """
        self._parent = parent
        self._children: List[MTGNode] = []
    
    @property
    def parent(self) -> Optional['MTGNode']:
        """Get the parent node."""
        return self._parent
    
    @parent.setter
    def parent(self, parent: Optional['MTGNode']):
        """Set the parent node."""
        self._parent = parent
    
    @property
    def children(self) -> List['MTGNode']:
        """Get the child nodes."""
        return self._children.copy()
    
    def add_child(self, child: 'MTGNode'):
        """
        Add a child node to this node.
        
        Args:
            child: The child node to add.
        """
        self._children.append(child)
        child.parent = self
    
    def remove_child(self, child: 'MTGNode'):
        """
        Remove a child node from this node.
        
        Args:
            child: The child node to remove.
        """
        if child in self._children:
            self._children.remove(child)
            child.parent = None
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the node to a dictionary representation.
        
        Returns:
            A dictionary representation of the node.
        """
        return {
            'type': self.__class__.__name__,
            'children': [child.to_dict() for child in self._children]
        }
    
    def __str__(self) -> str:
        """Return a string representation of the node."""
        return f"{self.__class__.__name__}"


class MTGDeclaration(MTGNode):
    """
    Represents declarations in MTG card text.
    
    Declarations define characteristics, create tokens, or establish
    card types, abilities, or other attributes.
    
    Examples:
    - "1/1 white Cat creature token"
    - "Flying"
    - "Vigilance"
    """
    
    def __init__(self, 
                 declaration_type: str, 
                 value: Optional[Any] = None, 
                 parent: Optional[MTGNode] = None):
        """
        Initialize an MTG declaration node.
        
        Args:
            declaration_type: The type of declaration (e.g., "keyword_ability", "token_creation").
            value: The value associated with the declaration, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(parent)
        self._declaration_type = declaration_type
        self._value = value
    
    @property
    def declaration_type(self) -> str:
        """Get the declaration type."""
        return self._declaration_type
    
    @declaration_type.setter
    def declaration_type(self, declaration_type: str):
        """Set the declaration type."""
        self._declaration_type = declaration_type
    
    @property
    def value(self) -> Optional[Any]:
        """Get the declaration value."""
        return self._value
    
    @value.setter
    def value(self, value: Optional[Any]):
        """Set the declaration value."""
        self._value = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the declaration to a dictionary representation."""
        result = super().to_dict()
        result.update({
            'declaration_type': self._declaration_type,
            'value': self._value
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the declaration."""
        if self._value:
            return f"{self.__class__.__name__}({self._declaration_type}, {self._value})"
        return f"{self.__class__.__name__}({self._declaration_type})"


class MTGStatement(MTGNode):
    """
    Represents statements in MTG card text.
    
    Statements describe conditional or triggered actions, static abilities,
    or rules text that reads like statements.
    
    Examples:
    - "If this creature dies, draw a card."
    - "Whenever you gain life, put a +1/+1 counter on this creature."
    - "You have hexproof."
    """
    
    class StatementType(Enum):
        """Enumeration of statement types in MTG card text."""
        TRIGGERED_ABILITY = "triggered_ability"
        STATIC_ABILITY = "static_ability"
        ACTIVATED_ABILITY = "activated_ability"
        CONDITIONAL = "conditional"
        REPLACEMENT = "replacement"
        COST_MODIFICATION = "cost_modification"
    
    def __init__(self, 
                 statement_type: Union[StatementType, str], 
                 condition: Optional[str] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize an MTG statement node.
        
        Args:
            statement_type: The type of statement.
            condition: The condition for the statement, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(parent)
        if isinstance(statement_type, str):
            try:
                self._statement_type = self.StatementType(statement_type)
            except ValueError:
                self._statement_type = statement_type
        else:
            self._statement_type = statement_type
        self._condition = condition
    
    @property
    def statement_type(self) -> Union[StatementType, str]:
        """Get the statement type."""
        return self._statement_type
    
    @statement_type.setter
    def statement_type(self, statement_type: Union[StatementType, str]):
        """Set the statement type."""
        if isinstance(statement_type, str):
            try:
                self._statement_type = self.StatementType(statement_type)
            except ValueError:
                self._statement_type = statement_type
        else:
            self._statement_type = statement_type
    
    @property
    def condition(self) -> Optional[str]:
        """Get the statement condition."""
        return self._condition
    
    @condition.setter
    def condition(self, condition: Optional[str]):
        """Set the statement condition."""
        self._condition = condition
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the statement to a dictionary representation."""
        result = super().to_dict()
        statement_type = self._statement_type.value if isinstance(self._statement_type, self.StatementType) else self._statement_type
        result.update({
            'statement_type': statement_type,
            'condition': self._condition
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the statement."""
        statement_type = self._statement_type.value if isinstance(self._statement_type, self.StatementType) else self._statement_type
        if self._condition:
            return f"{self.__class__.__name__}({statement_type}, {self._condition})"
        return f"{self.__class__.__name__}({statement_type})"


class MTGExpression(MTGNode):
    """
    Represents expressions in MTG card text.
    
    Expressions describe effects, costs, or target specifications.
    
    Examples:
    - "Destroy target creature"
    - "Draw a card"
    - "Target creature gets +2/+2 until end of turn"
    """
    
    class ExpressionType(Enum):
        """Enumeration of expression types in MTG card text."""
        ACTION = "action"
        EFFECT = "effect"
        TARGET = "target"
        COST = "cost"
        COUNTER = "counter"
        DURATION = "duration"
    
    def __init__(self, 
                 expression_type: Union[ExpressionType, str], 
                 value: Optional[Any] = None,
                 target: Optional[str] = None,
                 parent: Optional[MTGNode] = None):
        """
        Initialize an MTG expression node.
        
        Args:
            expression_type: The type of expression.
            value: The value associated with the expression, if any.
            target: The target of the expression, if any.
            parent: The parent node in the AST, if any.
        """
        super().__init__(parent)
        if isinstance(expression_type, str):
            try:
                self._expression_type = self.ExpressionType(expression_type)
            except ValueError:
                self._expression_type = expression_type
        else:
            self._expression_type = expression_type
        self._value = value
        self._target = target
    
    @property
    def expression_type(self) -> Union[ExpressionType, str]:
        """Get the expression type."""
        return self._expression_type
    
    @expression_type.setter
    def expression_type(self, expression_type: Union[ExpressionType, str]):
        """Set the expression type."""
        if isinstance(expression_type, str):
            try:
                self._expression_type = self.ExpressionType(expression_type)
            except ValueError:
                self._expression_type = expression_type
        else:
            self._expression_type = expression_type
    
    @property
    def value(self) -> Optional[Any]:
        """Get the expression value."""
        return self._value
    
    @value.setter
    def value(self, value: Optional[Any]):
        """Set the expression value."""
        self._value = value
    
    @property
    def target(self) -> Optional[str]:
        """Get the expression target."""
        return self._target
    
    @target.setter
    def target(self, target: Optional[str]):
        """Set the expression target."""
        self._target = target
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the expression to a dictionary representation."""
        result = super().to_dict()
        expression_type = self._expression_type.value if isinstance(self._expression_type, self.ExpressionType) else self._expression_type
        result.update({
            'expression_type': expression_type,
            'value': self._value,
            'target': self._target
        })
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the expression."""
        expression_type = self._expression_type.value if isinstance(self._expression_type, self.ExpressionType) else self._expression_type
        parts = [expression_type]
        if self._value is not None:
            parts.append(f"value={self._value}")
        if self._target is not None:
            parts.append(f"target={self._target}")
        return f"{self.__class__.__name__}({', '.join(parts)})"