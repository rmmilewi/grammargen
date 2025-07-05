# Magic: The Gathering Abstract Syntax Tree (AST)

This project implements a class hierarchy for representing Magic: The Gathering (MTG) card text in a structured, parseable form similar to how compilers represent source code.

## Class Hierarchy

The class hierarchy is designed to mirror programming language ASTs, with declarations, statements, and expressions:

### Base Classes

- **MTGNode**: Abstract base class for all nodes in the AST.
- **MTGDeclaration**: Represents declarations in MTG card text (e.g., keyword abilities, token creation).
- **MTGStatement**: Represents statements in MTG card text (e.g., triggered abilities, static abilities, conditional effects).
- **MTGExpression**: Represents expressions in MTG card text (e.g., effects, targets, costs).

### Specialized Classes

- **KeywordAbility**: Represents keyword abilities like "Flying", "First strike", etc. Can also represent keyword abilities granted to other objects.
- **TokenCreation**: Represents token creation effects.
- **TriggeredAbility**: Represents triggered abilities that start with "When" or "Whenever".
- **StaticAbility**: Represents static abilities that apply continuously.
- **ConditionalEffect**: Represents effects that depend on a condition.
- **TargetEffect**: Represents effects that target specific game objects.
- **CounterEffect**: Represents effects that add or remove counters.
- **CostModification**: Represents modifications to spell costs.
- **ActivatedAbility**: Represents activated abilities with costs and effects.
- **ConditionalTriggeredAbility**: Represents triggered abilities with additional conditions.
- **SpellSequence**: Represents sequences of spell effects that happen in order.
- **VariableCostModification**: Represents cost modifications with variable components.

### Utility Classes

- **MTGCardRoot**: Concrete implementation of MTGNode to serve as the root node for MTG card ASTs.
- **MTGCardBuilder**: Builder class to simplify the construction of MTG card ASTs.

## Usage

### Basic Usage

```python
from mtg_ast_builder import MTGCardBuilder

# Create a builder
builder = MTGCardBuilder()

# Add keyword abilities
builder.add_keyword_ability("Flying")
builder.add_keyword_ability("Vigilance")

# Build the AST
card_ast = builder.build()

# Convert to dictionary representation
card_dict = builder.to_dict()
```

### Complex Example

```python
from mtg_ast import MTGExpression
from mtg_ast_builder import MTGCardBuilder
from mtg_ast_specialized import TokenCreation

# Create a builder
builder = MTGCardBuilder()

# Add a keyword ability
builder.add_keyword_ability("Lifelink")

# Add a triggered ability
trigger = "when this creature enters"
token_effect = MTGExpression(MTGExpression.ExpressionType.ACTION, "create tokens")
triggered_ability = builder.add_triggered_ability(trigger, token_effect)

# Add a token creation as a child of the triggered ability
token = TokenCreation(3, 3, ["white"], ["creature"], ["Knight"], 2)
triggered_ability.add_child(token)

# Build the AST
card_ast = builder.build()
```

### New Functionality Examples

```python
# Activated ability
builder.add_activated_ability("{T}", "Add {G} for each Elf you control")

# Conditional triggered ability
builder.add_conditional_triggered_ability(
    trigger="when this enchantment enters",
    condition="if you control a creature with power 4 or greater",
    effect=MTGExpression(MTGExpression.ExpressionType.ACTION, "draw 1 card")
)

# Keyword ability with target
builder.add_keyword_ability("Trample", "Reminder text", target="creatures you control")

# Variable cost modification
builder.add_variable_cost_modification(
    modification_type="reduce",
    cost="{X}",
    variable_definition="where X is the total power of creatures you control"
)

# Spell sequence
builder.add_spell_sequence([
    {"type": "reveal", "target": "top X cards of your library"},
    {"type": "optional_put", "target": "battlefield", "restriction": "permanent cards"},
    {"type": "put", "target": "graveyard", "source": "remaining cards"}
])
```

## Testing

The project includes comprehensive unit tests for all classes and functionality. Run the tests using pytest:

```bash
python -m pytest mtg-ast-test/tests/ -v
```

## Future Work

This implementation focuses on the class design, not on parsing text into this structure. Future work could include:

1. Implementing a parser to convert MTG card text into this AST structure.
2. Adding more specialized node types for specific MTG mechanics.
3. Implementing a visitor pattern for traversing and manipulating the AST.
4. Adding serialization/deserialization to JSON or other formats.