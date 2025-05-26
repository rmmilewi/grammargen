import argparse
import importlib
import re
from lark import Lark, UnexpectedInput
from lark.reconstruct import Reconstructor

def load_grammar(grammar_path: str) -> str:
    with open(grammar_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_inputs_and_targets_from_file(file_path: str) -> list[tuple[str, str | None]]:
    """
    Extracts inputs (and optionally targets) from a file where each record is enclosed in triple quotes.

    Lines with a comma between two triple-quoted blocks are treated as input/output pairs.
    Newlines within blocks are preserved and trimmed. Outputs may be None if not provided.

    Returns:
        List of tuples: (input_string, output_string or None)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Matches pairs: """...""","""...""" OR single: """..."""
    pattern = re.compile(
        r'"""(.*?)"""\s*,\s*"""(.*?)"""|'   # Input/output pair
        r'"""(.*?)"""',                    # Or single input
        re.DOTALL
    )

    results = []
    for match in pattern.finditer(content):
        if match.group(1) and match.group(2):
            input_str = match.group(1).strip()
            output_str = match.group(2).strip()
            results.append((input_str, output_str))
        else:
            input_str = match.group(3).strip()
            results.append((input_str, None))

    return results


def load_transformer(import_path: str):
    """
    Dynamically imports a transformer class from the given module path.

    Args:
        import_path (str): The dot-separated import path (e.g., "cases.morse.transformer").

    Returns:
        An instance of the Transformer class from the imported module.
    """
    try:
        module = importlib.import_module(import_path)
        return module.LarkTransformer()
    except (ModuleNotFoundError, AttributeError) as e:
        raise ImportError(f"Could not import/instantiate Transformer from '{import_path}': {e}")

def main():
    parser = argparse.ArgumentParser(description="Lark Grammar Parser Driver")
    parser.add_argument("--grammar_file", help="Path to the grammar file (e.g., cases/morse/grammar.lark)")
    parser.add_argument("--input_file", nargs="?", default=None, help="Path to the input text to parse (optional)")
    parser.add_argument("--transformer", nargs="?", default=None, help="Import path for the transformer if required for case (e.g., cases.morse.transformer)")
    parser.add_argument("--start", default="start", help="Start symbol in the grammar (default: 'start')")
    parser.add_argument("--parser", nargs="?", choices=["earley", "lalr", "cyk"], default="earley",
                        help="Parser algorithm to use (default: earley)")

    args = parser.parse_args()

    grammar_text = load_grammar(args.grammar_file)
    print(f"Loaded grammar from '{args.grammar_file}' using start rule '{args.start}' with parser '{args.parser}'")

    try:
        lark_parser = Lark(grammar_text, start=args.start, parser=args.parser,maybe_placeholders=False)
        print("Parser successfully constructed.\n")
    except Exception as e:
        print("An error occurred while building the parser...")
        raise e
    #reconstructor = Reconstructor(lark_parser,term_subs=None)

    transformer = None
    if args.transformer:
        transformer = load_transformer(args.transformer)

    if args.input_file:
        stringsAndTargetsToParse = extract_inputs_and_targets_from_file(args.input_file)
        countOfStringsParsedSuccessfully = 0
        countOfStringsTransformedSuccessfully = 0
        for i in range(len(stringsAndTargetsToParse)):
            stringAndTarget = stringsAndTargetsToParse[i]
            print("-----------------------")
            print("Parsing ({current}/{total})...".format(current=i+1,total=len(stringsAndTargetsToParse)))
            print("\"\"\"",stringAndTarget[0],"\"\"\"")
            try:
                tree = lark_parser.parse(stringAndTarget[0])
                #print("RECONSTRUCTION:",reconstructor.reconstruct(tree))
                countOfStringsParsedSuccessfully += 1
            except Exception as e:
                print("Error encountered during parsing...")
                print(e)

                if transformer != None:
                    try:
                        output = transformer.transform(tree)
                        if output == stringAndTarget[1]:
                            print("Transformer output '{output}' matches target '{target}'".format(output=output,target=stringAndTarget[1]))
                            countOfStringsTransformedSuccessfully +=1
                        else:
                            print("Transformer output '{output}' does NOT match target '{target}'".format(output=output,target=stringAndTarget[1]))

                    except Exception as e:
                        print("Error encountered during transformation of parse tree...")
                        print(e)
            print("-----------------------")
        print("Total number of strings correctly parsed: {successes}/{total}".format(successes=countOfStringsParsedSuccessfully,total=len(stringsAndTargetsToParse)))
        if transformer != None:
            print("Total number of strings correctly transformed: {successes}/{total}".format(successes=countOfStringsTransformedSuccessfully, total=len(stringsAndTargetsToParse)))
    else:
        print("No input file provided. Parser construction only.")

if __name__ == "__main__":
    main()