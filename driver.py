import argparse
import importlib
import re
import multiprocessing
import time
import os
from multiprocessing import Pool, Manager, Value
from lark import Lark, UnexpectedInput

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

# Global variables for multiprocessing
_GRAMMAR_TEXT = None
_START_RULE = None
_PARSER_TYPE = None
_TRANSFORMER_PATH = None
_COUNTER = None
_TOTAL = None

def initialize_worker(grammar_text, start_rule, parser_type, transformer_path, counter, total):
    """
    Initialize the worker process with the grammar and transformer.
    This function sets global variables that will be used by process_input.
    """
    global _GRAMMAR_TEXT, _START_RULE, _PARSER_TYPE, _TRANSFORMER_PATH, _COUNTER, _TOTAL
    _GRAMMAR_TEXT = grammar_text
    _START_RULE = start_rule
    _PARSER_TYPE = parser_type
    _TRANSFORMER_PATH = transformer_path
    _COUNTER = counter
    _TOTAL = total

def process_input(args):
    """
    Process a single input string with the parser and transformer.
    
    Args:
        args: A tuple containing (index, input_string, target)
        
    Returns:
        A dictionary containing the results of parsing and transformation
    """
    global _GRAMMAR_TEXT, _START_RULE, _PARSER_TYPE, _TRANSFORMER_PATH, _COUNTER, _TOTAL
    
    i, string_and_target = args
    input_str, target = string_and_target
    
    result = {
        "index": i,
        "input": input_str,
        "parsed_successfully": False,
        "transformed_successfully": False,
        "parse_error": None,
        "transform_error": None,
        "tree_pretty": None,  # Store the pretty-printed tree as string
        "output": None
    }
    
    # Create parser in this process
    try:
        lark_parser = Lark(_GRAMMAR_TEXT, start=_START_RULE, parser=_PARSER_TYPE, maybe_placeholders=False)
    except Exception as e:
        result["parse_error"] = f"Parser initialization error: {str(e)}"
        with _COUNTER.get_lock():
            _COUNTER.value += 1
        return result
    
    # Create transformer in this process if needed
    transformer = None
    if _TRANSFORMER_PATH:
        try:
            transformer = load_transformer(_TRANSFORMER_PATH)
        except Exception as e:
            result["transform_error"] = f"Transformer initialization error: {str(e)}"
    
    # Parse the input
    try:
        tree = lark_parser.parse(input_str)
        result["parsed_successfully"] = True
        result["tree_pretty"] = tree.pretty()  # Store pretty-printed tree
    except Exception as e:
        result["parsed_successfully"] = False
        result["parse_error"] = str(e)
        with _COUNTER.get_lock():
            _COUNTER.value += 1
        return result
    
    # Transform if needed
    if transformer is not None and result["parsed_successfully"]:
        try:
            output = transformer.transform(tree)
            result["output"] = output
            if output == target:
                result["transformed_successfully"] = True
        except Exception as e:
            result["transform_error"] = str(e)
    
    # Update progress counter
    with _COUNTER.get_lock():
        _COUNTER.value += 1
        current = _COUNTER.value
        if current % 10 == 0 or current == _TOTAL.value:
            percent = (current / _TOTAL.value) * 100
            print(f"\rProgress: {current}/{_TOTAL.value} ({percent:.1f}%)", end="", flush=True)
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Lark Grammar Parser Driver")
    parser.add_argument("--grammar_file", help="Path to the grammar file (e.g., cases/morse/grammar.lark)")
    parser.add_argument("--input_file", nargs="?", default=None, help="Path to the input text to parse (optional)")
    parser.add_argument("--transformer", nargs="?", default=None, help="Import path for the transformer if required for case (e.g., cases.morse.transformer)")
    parser.add_argument("--start", default="start", help="Start symbol in the grammar (default: 'start')")
    parser.add_argument("--parser", nargs="?", choices=["earley", "lalr", "cyk"], default="earley",
                        help="Parser algorithm to use (default: earley)")
    parser.add_argument("--processes", type=int, default=None, 
                        help="Number of processes to use for parallel parsing (default: number of CPU cores)")
    parser.add_argument("--batch_size", type=int, default=None,
                        help="Number of inputs to process in each batch (default: all at once)")
    parser.add_argument("--verbose", action="store_true", 
                        help="Print detailed output for each parsed input")

    args = parser.parse_args()

    # Determine number of processes to use
    num_processes = args.processes if args.processes else multiprocessing.cpu_count()
    
    grammar_text = load_grammar(args.grammar_file)
    print(f"Loaded grammar from '{args.grammar_file}' using start rule '{args.start}' with parser '{args.parser}'")
    print(f"Using {num_processes} processes for parallel parsing")

    # Test parser construction in the main process to catch any immediate errors
    try:
        lark_parser = Lark(grammar_text, start=args.start, parser=args.parser, maybe_placeholders=False)
        print("Parser successfully constructed.\n")
    except Exception as e:
        print("An error occurred while building the parser...")
        raise e

    if args.input_file:
        strings_and_targets = extract_inputs_and_targets_from_file(args.input_file)
        total_inputs = len(strings_and_targets)
        print(f"Processing {total_inputs} inputs...")
        
        # Create shared counter for progress tracking
        counter = Value('i', 0)
        total_val = Value('i', total_inputs)
        
        # Prepare arguments for parallel processing - just pass indices and input/target pairs
        process_args = [(i, strings_and_targets[i]) for i in range(total_inputs)]
        
        # Process in batches if requested
        batch_size = args.batch_size if args.batch_size else total_inputs
        
        start_time = time.time()
        all_results = []
        
        for batch_start in range(0, total_inputs, batch_size):
            batch_end = min(batch_start + batch_size, total_inputs)
            batch_args = process_args[batch_start:batch_end]
            
            if batch_size < total_inputs:
                print(f"\nProcessing batch {batch_start//batch_size + 1}/{(total_inputs + batch_size - 1)//batch_size}: "
                      f"inputs {batch_start+1}-{batch_end} of {total_inputs}")
            
            # Process inputs in parallel with initialization
            with Pool(
                processes=num_processes,
                initializer=initialize_worker,
                initargs=(grammar_text, args.start, args.parser, args.transformer, counter, total_val)
            ) as pool:
                batch_results = pool.map(process_input, batch_args)
                all_results.extend(batch_results)
                
        # Print newline after progress updates
        print("\n")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Parsing completed in {elapsed_time:.2f} seconds")
        
        # Sort results by index to maintain original order
        all_results.sort(key=lambda x: x["index"])
        
        # Display results and count successes
        count_parsed_successfully = 0
        count_transformed_successfully = 0
        
        for result in all_results:
            if result["parsed_successfully"]:
                count_parsed_successfully += 1
                if args.transformer is not None and result["transformed_successfully"]:
                    count_transformed_successfully += 1
        
        # Print detailed results if verbose mode is enabled
        if args.verbose:
            for result in all_results:
                i = result["index"]
                input_str = result["input"]
                
                print("-----------------------")
                print(f"Parsing ({i+1}/{total_inputs})...")
                print(f"\"\"\"{input_str}\"\"\"")
                
                if result["parsed_successfully"]:
                    print(result["tree_pretty"])  # Use the pretty-printed tree string
                else:
                    print("Error encountered during parsing...")
                    parsing_error_message = result["parse_error"]
                    if parsing_error_message and "Expected one of:" in parsing_error_message:
                        split_error_message = parsing_error_message.split("Expected one of:")
                        if len(split_error_message[1]) >= 100:
                            print(split_error_message[0], "Expected one of:\n", split_error_message[1][0:100], "\n\t...")
                        else:
                            print(parsing_error_message)
                    else:
                        print(parsing_error_message)
                
                if args.transformer is not None and result["parsed_successfully"]:
                    if result["transform_error"] is None:
                        output = result["output"]
                        target = strings_and_targets[i][1]
                        if result["transformed_successfully"]:
                            print(f"Transformer output '{output}' matches target '{target}'")
                        else:
                            print(f"Transformer output '{output}' does NOT match target '{target}'")
                    else:
                        print("Error encountered during transformation of parse tree...")
                        print(result["transform_error"])
                
                print("-----------------------")
        
        print(f"Total number of strings correctly parsed: {count_parsed_successfully}/{total_inputs}")
        if args.transformer is not None:
            print(f"Total number of strings correctly transformed: {count_transformed_successfully}/{total_inputs}")
    else:
        print("No input file provided. Parser construction only.")

if __name__ == "__main__":
    main()