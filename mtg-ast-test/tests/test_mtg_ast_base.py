"""
Unit tests for the base MTG AST classes.
"""
import sys
import os
import unittest
from typing import List, Optional, Dict, Any

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtg_ast import MTGNode, MTGDeclaration, MTGStatement, MTGExpression


class TestMTGNode(unittest.TestCase):
    """Test cases for the MTGNode class."""
    
    # Create a concrete subclass for testing
    class ConcreteNode(MTGNode):
        def to_dict(self):
            return super().to_dict()
    
    def test_parent_child_relationship(self):
        """Test parent-child relationship between nodes."""
        parent = self.ConcreteNode()
        child = self.ConcreteNode(parent)
        parent.add_child(child)
        
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.children)
    
    def test_remove_child(self):
        """Test removing a child node."""
        parent = self.ConcreteNode()
        child = self.ConcreteNode(parent)
        parent.add_child(child)
        parent.remove_child(child)
        
        self.assertIsNone(child.parent)
        self.assertNotIn(child, parent.children)
    
    def test_to_dict(self):
        """Test converting a node to a dictionary."""
        node = self.ConcreteNode()
        child = self.ConcreteNode()
        node.add_child(child)
        
        node_dict = node.to_dict()
        self.assertEqual(node_dict['type'], 'ConcreteNode')
        self.assertEqual(len(node_dict['children']), 1)
        self.assertEqual(node_dict['children'][0]['type'], 'ConcreteNode')


class TestMTGDeclaration(unittest.TestCase):
    """Test cases for the MTGDeclaration class."""
    
    def test_initialization(self):
        """Test initializing a declaration."""
        declaration = MTGDeclaration("keyword_ability", "Flying")
        
        self.assertEqual(declaration.declaration_type, "keyword_ability")
        self.assertEqual(declaration.value, "Flying")
    
    def test_setters(self):
        """Test setting declaration properties."""
        declaration = MTGDeclaration("keyword_ability", "Flying")
        declaration.declaration_type = "token_creation"
        declaration.value = {"power": 1, "toughness": 1}
        
        self.assertEqual(declaration.declaration_type, "token_creation")
        self.assertEqual(declaration.value, {"power": 1, "toughness": 1})
    
    def test_to_dict(self):
        """Test converting a declaration to a dictionary."""
        declaration = MTGDeclaration("keyword_ability", "Flying")
        
        declaration_dict = declaration.to_dict()
        self.assertEqual(declaration_dict['type'], 'MTGDeclaration')
        self.assertEqual(declaration_dict['declaration_type'], 'keyword_ability')
        self.assertEqual(declaration_dict['value'], 'Flying')


class TestMTGStatement(unittest.TestCase):
    """Test cases for the MTGStatement class."""
    
    def test_initialization(self):
        """Test initializing a statement."""
        statement = MTGStatement(MTGStatement.StatementType.TRIGGERED_ABILITY, "when this creature enters the battlefield")
        
        self.assertEqual(statement.statement_type, MTGStatement.StatementType.TRIGGERED_ABILITY)
        self.assertEqual(statement.condition, "when this creature enters the battlefield")
    
    def test_initialization_with_string(self):
        """Test initializing a statement with a string statement type."""
        statement = MTGStatement("triggered_ability", "when this creature enters the battlefield")
        
        self.assertEqual(statement.statement_type, MTGStatement.StatementType.TRIGGERED_ABILITY)
        self.assertEqual(statement.condition, "when this creature enters the battlefield")
    
    def test_setters(self):
        """Test setting statement properties."""
        statement = MTGStatement(MTGStatement.StatementType.TRIGGERED_ABILITY, "when this creature enters the battlefield")
        statement.statement_type = MTGStatement.StatementType.STATIC_ABILITY
        statement.condition = None
        
        self.assertEqual(statement.statement_type, MTGStatement.StatementType.STATIC_ABILITY)
        self.assertIsNone(statement.condition)
    
    def test_to_dict(self):
        """Test converting a statement to a dictionary."""
        statement = MTGStatement(MTGStatement.StatementType.TRIGGERED_ABILITY, "when this creature enters the battlefield")
        
        statement_dict = statement.to_dict()
        self.assertEqual(statement_dict['type'], 'MTGStatement')
        self.assertEqual(statement_dict['statement_type'], 'triggered_ability')
        self.assertEqual(statement_dict['condition'], 'when this creature enters the battlefield')


class TestMTGExpression(unittest.TestCase):
    """Test cases for the MTGExpression class."""
    
    def test_initialization(self):
        """Test initializing an expression."""
        expression = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card", "you")
        
        self.assertEqual(expression.expression_type, MTGExpression.ExpressionType.ACTION)
        self.assertEqual(expression.value, "draw a card")
        self.assertEqual(expression.target, "you")
    
    def test_initialization_with_string(self):
        """Test initializing an expression with a string expression type."""
        expression = MTGExpression("action", "draw a card", "you")
        
        self.assertEqual(expression.expression_type, MTGExpression.ExpressionType.ACTION)
        self.assertEqual(expression.value, "draw a card")
        self.assertEqual(expression.target, "you")
    
    def test_setters(self):
        """Test setting expression properties."""
        expression = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card", "you")
        expression.expression_type = MTGExpression.ExpressionType.EFFECT
        expression.value = "gain 3 life"
        expression.target = "target player"
        
        self.assertEqual(expression.expression_type, MTGExpression.ExpressionType.EFFECT)
        self.assertEqual(expression.value, "gain 3 life")
        self.assertEqual(expression.target, "target player")
    
    def test_to_dict(self):
        """Test converting an expression to a dictionary."""
        expression = MTGExpression(MTGExpression.ExpressionType.ACTION, "draw a card", "you")
        
        expression_dict = expression.to_dict()
        self.assertEqual(expression_dict['type'], 'MTGExpression')
        self.assertEqual(expression_dict['expression_type'], 'action')
        self.assertEqual(expression_dict['value'], 'draw a card')
        self.assertEqual(expression_dict['target'], 'you')


if __name__ == '__main__':
    unittest.main()