from lark import Transformer

class LarkTransformer(Transformer):
    """Create a transformer that takes in a string of the form a^n b^m c^o and returns YES
    if n==m==o (e.g., aaabbbccc) and NO otherwise (e.g., aaaabcc).
    """""
    def start(self,children):
        print(children)
        a_sequence_length = children[0]
        b_sequence_length = children[1]
        c_sequence_length = children[2]
        if a_sequence_length == b_sequence_length and b_sequence_length == c_sequence_length:
            return "YES"
        else:
            return "NO"

    def a_rule(self,children):
        return len(children)

    def b_rule(self,children):
        return len(children)

    def c_rule(self,children):
        return len(children)

