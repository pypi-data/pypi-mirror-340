import unittest
from cipherShad0w.core import Sort, DoublyCircularLinkedList, DeterministicFiniteAutomaton, PushdownAutomaton

class TestSortingVisualizer(unittest.TestCase):
    def test_bubble_sort(self) -> None:
        sorter = Sort([4, 2, 3, 1])
        sorted_array, _ = sorter.bubble_sort()
        self.assertEqual(sorted_array, [1, 2, 3, 4])

    def test_quick_sort(self) -> None:
        sorter = Sort([4, 2, 3, 1])
        sorted_array, _ = sorter.quick_sort()
        self.assertEqual(sorted_array, [1, 2, 3, 4])

class TestDoublyCircularLinkedList(unittest.TestCase):
    def test_append_and_display(self) -> None:
        dll = DoublyCircularLinkedList()
        dll.append(1)
        dll.append(2)
        dll.append(3)
        self.assertEqual(dll.display(), [1, 2, 3])

    def test_delete(self) -> None:
        dll = DoublyCircularLinkedList()
        dll.append(1)
        dll.append(2)
        dll.append(3)
        dll.delete(2)
        self.assertEqual(dll.display(), [1, 3])

class TestDeterministicFiniteAutomaton(unittest.TestCase):
    def test_accepts(self) -> None:
        states: set[str] = {"q0", "q1"}
        alphabet: set[str] = {"0", "1"}
        transition_function: dict[tuple[str, str], str] = {
            ("q0", "0"): "q0",
            ("q0", "1"): "q1",
            ("q1", "0"): "q1",
            ("q1", "1"): "q0",
        }
        start_state = "q0"
        accept_states = {"q1"}

        dfa = DeterministicFiniteAutomaton(states, alphabet, transition_function, start_state, accept_states)
        self.assertTrue(dfa.accepts("01"))
        self.assertFalse(dfa.accepts("00"))

class TestPushdownAutomaton(unittest.TestCase):
    def test_accepts(self) -> None:
        states: set[str] = {"q0", "q1", "q2"}
        alphabet: set[str] = {"a", "b"}
        stack_alphabet: set[str] = {"A", "$"}
        transition_function = {
            ("q0", "a", "$"): ("q0", ["A", "$"]),
            ("q0", "a", "A"): ("q0", ["A", "A"]),
            ("q0", "b", "A"): ("q1", []),
            ("q1", "b", "A"): ("q1", []),
            ("q1", "", "$"): ("q2", []),
        }
        start_state = "q0"
        start_stack_symbol = "$"
        accept_states: set[str] = {"q2"}

        pda = PushdownAutomaton(states, alphabet, stack_alphabet, transition_function, start_state, start_stack_symbol, accept_states)
        self.assertTrue(pda.accepts("aaabbb"))
        self.assertFalse(pda.accepts("aab"))

if __name__ == "__main__":
    unittest.main()
