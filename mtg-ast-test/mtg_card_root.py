"""
Root node for MTG card ASTs.

This module provides a concrete implementation of the MTGNode class
to serve as the root node for MTG card ASTs.
"""
from typing import List, Optional, Dict, Any
from mtg_ast import MTGNode


class MTGCardRoot(MTGNode):
    """
    Concrete implementation of MTGNode to serve as the root node for MTG card ASTs.
    
    This class provides a concrete implementation of the abstract MTGNode class
    to serve as the root node for MTG card ASTs.
    """
    
    def __init__(self, parent: Optional[MTGNode] = None):
        """
        Initialize an MTG card root node.
        
        Args:
            parent: The parent node in the AST, if any.
        """
        super().__init__(parent)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the node to a dictionary representation.
        
        Returns:
            A dictionary representation of the node.
        """
        return {
            'type': 'MTGCardRoot',
            'children': [child.to_dict() for child in self.children]
        }