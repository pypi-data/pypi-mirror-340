import argparse
import inspect
from .core import Sort, DoublyLinkedList, Pushdown

def display_help():
    """
    Display information about the available commands and their usage.
    """
    help_text = """
        CipherShad0w CLI - Available Commands:

        1. Sorting Operations:
        Sort an array using a specific algorithm.
        Usage:
            cipherShad0w sort -a <array> -alg <algorithm>
        Example:
            cipherShad0w sort -a 7 2 5 1 9 -alg bubble

        Supported algorithms:
            - bubble
            - quick
            - merge
            - heap
            - shell
            - radix
            - selection
            - insertion
            - counting
            - bucket
            - cocktail

        2. Retrieve Source Code:
        Get the source code of a specific algorithm or class.
        Usage:
            cipherShad0w get <target>
        Example:
            cipherShad0w get bubble
            cipherShad0w get all
            cipherShad0w get DoublyLinkedList
            cipherShad0w get Pushdown

        3. Doubly Linked List Operations:
        Perform operations on a doubly linked list.
        Usage:
            cipherShad0w dll <operation> -d <data>
        Example:
            cipherShad0w dll append -d 10
            cipherShad0w dll display

        Supported operations:
            - append
            - prepend
            - delete
            - display
            - search

        4. Pushdown Automaton Simulation:
        Simulate a pushdown automaton with an input string.
        Usage:
            cipherShad0w pda -i <input_string>
        Example:
            cipherShad0w pda -i "aab"

        For more details, refer to the documentation or use the commands as shown above.
    """
    print(help_text)

def main() -> None:
    """
    Main function to handle the CipherShad0w CLI commands.
    """
    # Main parser for the CLI
    parser = argparse.ArgumentParser(description="CipherShad0w CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for sorting operations
    sort_parser = subparsers.add_parser("sort", help="Sort an array")
    sort_parser.add_argument("-a", "--array", type=int, nargs="+", required=True, help="Array (e.g., 7 2 5)")
    sort_parser.add_argument(
        "-alg", "--algorithm",
        choices=["bubble", "quick", "merge", "heap", "shell", "radix", "selection", "insertion", "counting", "bucket", "cocktail"],
        default="bubble",
        help="Sorting algorithm"
    )

    # Subparser for retrieving code
    get_parser = subparsers.add_parser("get", help="Get the code of a class or method")
    get_parser.add_argument(
        "target",
        choices=["bubble", "quick", "merge", "heap", "shell", "radix", "selection", "insertion", "counting", "bucket", "cocktail", "all", "DoublyLinkedList", "Pushdown"],
        help="Target to get code for"
    )

    # Subparser for DoublyLinkedList operations
    dll_parser = subparsers.add_parser("dll", help="Operate on a DoublyLinkedList")
    dll_parser.add_argument("operation", choices=["append", "prepend", "delete", "display", "search"], help="Operation to perform")
    dll_parser.add_argument("-d", "--data", type=int, help="Data for the operation")

    # Subparser for Pushdown Automaton operations
    pda_parser = subparsers.add_parser("pda", help="Operate on a Pushdown Automaton")
    pda_parser.add_argument("-i", "--input", type=str, required=True, help="Input string for the automaton")

    # Subparser for displaying help
    help_parser = subparsers.add_parser("help", help="Display help information")

    # Parse arguments
    args: argparse.Namespace = parser.parse_args()

    if args.command == "sort":
        # Execute sorting operations
        sv = Sort(args.array)
        if args.algorithm == "bubble":
            sorted_arr, steps = sv.bubble_sort()
        elif args.algorithm == "quick":
            sorted_arr, steps = sv.quick_sort()
        elif args.algorithm == "merge":
            sorted_arr, steps = sv.merge_sort()
        elif args.algorithm == "heap":
            sorted_arr, steps = sv.heap_sort()
        elif args.algorithm == "shell":
            sorted_arr, steps = sv.shell_sort()
        elif args.algorithm == "radix":
            sorted_arr, steps = sv.radix_sort()
        elif args.algorithm == "selection":
            sorted_arr, steps = sv.selection_sort()
        elif args.algorithm == "insertion":
            sorted_arr, steps = sv.insertion_sort()
        elif args.algorithm == "counting":
            sorted_arr, steps = sv.counting_sort()
        elif args.algorithm == "bucket":
            sorted_arr, steps = sv.bucket_sort()
        elif args.algorithm == "cocktail":
            sorted_arr, steps = sv.cocktail_sort()
        else:
            sorted_arr, steps = sv.bubble_sort()

        # Output the result
        print(f"\nResult ({args.algorithm}): {sorted_arr}")
        print(f"Steps: {len(steps)}")

    elif args.command == "get":
        # Retrieve the source code of a method or class
        if args.target in ["bubble", "quick", "merge", "heap", "shell", "radix", "selection", "insertion", "counting", "bucket", "cocktail", "all"]:
            sv = Sort([])
            if args.target == "all":
                code = inspect.getsource(Sort)  # Retrieve the entire Sort class code
            else:
                code = inspect.getsource(getattr(sv, f"{args.target}_sort"))  # Retrieve specific method code
        elif args.target == "DoublyLinkedList":
            code = inspect.getsource(DoublyLinkedList)  # Retrieve DoublyLinkedList class code
        elif args.target == "Pushdown":
            code = inspect.getsource(Pushdown)  # Retrieve Pushdown class code
        else:
            code = "Target not found."
        
        # Output the source code
        print(f"\nCode for {args.target}:\n")
        print(code)

    elif args.command == "dll":
        # Execute DoublyLinkedList operations
        dll = DoublyLinkedList()
        if args.operation == "append":
            dll.append(args.data)  # Append data
            print(f"Appended {args.data} to the list.")
        elif args.operation == "prepend":
            dll.prepend(args.data)  # Prepend data
            print(f"Prepended {args.data} to the list.")
        elif args.operation == "delete":
            dll.delete(args.data)  # Delete data
            print(f"Deleted {args.data} from the list.")
        elif args.operation == "display":
            print(f"List contents: {dll.display()}")  # Display the list
        elif args.operation == "search":
            found = dll.search(args.data)  # Search for data
            print(f"Search result for {args.data}: {'Found' if found else 'Not Found'}")

    elif args.command == "pda":
        # Example Pushdown Automaton
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        stack_alphabet = {"$", "A"}
        transition_function = {
            ("q0", "a", "$"): ("q1", ["A", "$"]),
            ("q1", "a", "A"): ("q1", ["A", "A"]),
            ("q1", "b", "A"): ("q2", []),
            ("q2", "", "$"): ("q2", [])
        }
        start_state = "q0"
        start_stack_symbol = "$"
        accept_states = {"q2"}

        # Initialize Pushdown Automaton
        pda = Pushdown(states, alphabet, stack_alphabet, transition_function, start_state, start_stack_symbol, accept_states)
        result = pda.accepts(args.input)  # Check the input
        print(f"Input '{args.input}' is {'accepted' if result else 'rejected'} by the Pushdown Automaton.")

    elif args.command == "help":
        # Display help information
        display_help()

if __name__ == "__main__":
    main()
