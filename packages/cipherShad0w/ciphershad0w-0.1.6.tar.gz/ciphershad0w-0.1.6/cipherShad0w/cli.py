import argparse
import inspect
from .core import Sort, DoublyLinkedList, Pushdown

def main() -> None:
    # Hauptparser für die CLI
    parser = argparse.ArgumentParser(description="CipherShad0w CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser für Sortieroperationen
    sort_parser = subparsers.add_parser("sort", help="Sort an array")
    sort_parser.add_argument("-a", "--array", type=int, nargs="+", required=True, help="Array (z.B. 7 2 5)")
    sort_parser.add_argument("-alg", "--algorithm", choices=["bubble", "quick", "merge", "heap", "shell", "radix"], default="bubble", help="Sorting algorithm")

    # Subparser für das Abrufen von Code
    get_parser = subparsers.add_parser("get", help="Get the code of a class or method")
    get_parser.add_argument("target", choices=["bubble", "quick", "merge", "heap", "shell", "radix", "all", "DoublyLinkedList", "Pushdown"], help="Target to get code for")

    # Subparser für DoublyLinkedList-Operationen
    dll_parser = subparsers.add_parser("dll", help="Operate on a DoublyLinkedList")
    dll_parser.add_argument("operation", choices=["append", "prepend", "delete", "display", "search"], help="Operation to perform")
    dll_parser.add_argument("-d", "--data", type=int, help="Data for the operation")

    # Subparser für Pushdown-Automaten-Operationen
    pda_parser = subparsers.add_parser("pda", help="Operate on a Pushdown Automaton")
    pda_parser.add_argument("-i", "--input", type=str, required=True, help="Input string for the automaton")

    # Argumente parsen
    args: argparse.Namespace = parser.parse_args()

    if args.command == "sort":
        # Sortieroperationen ausführen
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
        else:
            sorted_arr, steps = sv.bubble_sort()

        # Ergebnis ausgeben
        print(f"\nResult ({args.algorithm}): {sorted_arr}")
        print(f"Steps: {len(steps)}")

    elif args.command == "get":
        # Quellcode einer Methode oder Klasse abrufen
        if args.target in ["bubble", "quick", "merge", "heap", "shell", "radix", "all"]:
            sv = Sort([])
            if args.target == "all":
                code = inspect.getsource(Sort)  # Gesamten Code der Sort-Klasse abrufen
            else:
                code = inspect.getsource(getattr(sv, f"{args.target}_sort"))  # Code einer spezifischen Methode abrufen
        elif args.target == "DoublyLinkedList":
            code = inspect.getsource(DoublyLinkedList)  # Code der DoublyLinkedList-Klasse abrufen
        elif args.target == "Pushdown":
            code = inspect.getsource(Pushdown)  # Code der Pushdown-Klasse abrufen
        else:
            code = "Target not found."
        
        # Quellcode ausgeben
        print(f"\nCode for {args.target}:\n")
        print(code)

    elif args.command == "dll":
        # DoublyLinkedList-Operationen ausführen
        dll = DoublyLinkedList()
        if args.operation == "append":
            dll.append(args.data)  # Daten anhängen
            print(f"Appended {args.data} to the list.")
        elif args.operation == "prepend":
            dll.prepend(args.data)  # Daten voranstellen
            print(f"Prepended {args.data} to the list.")
        elif args.operation == "delete":
            dll.delete(args.data)  # Daten löschen
            print(f"Deleted {args.data} from the list.")
        elif args.operation == "display":
            print(f"List contents: {dll.display()}")  # Liste anzeigen
        elif args.operation == "search":
            found = dll.search(args.data)  # Nach Daten suchen
            print(f"Search result for {args.data}: {'Found' if found else 'Not Found'}")

    elif args.command == "pda":
        # Beispiel für einen Pushdown-Automaten
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

        # Pushdown-Automat initialisieren
        pda = Pushdown(states, alphabet, stack_alphabet, transition_function, start_state, start_stack_symbol, accept_states)
        result = pda.accepts(args.input)  # Eingabe prüfen
        print(f"Input '{args.input}' is {'accepted' if result else 'rejected'} by the Pushdown Automaton.")

if __name__ == "__main__":
    main()
