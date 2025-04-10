class Sort:
    """
    A class to perform various sorting algorithms and record the steps for visualization.
    """

    def __init__(self, arr=None):
        """
        Initialize the Sort class with an optional array.

        :param arr: List of integers to sort.
        """
        self.original = arr.copy() if arr else []  # Store the original array
        self.array = arr.copy() if arr else []  # Working copy of the array
        self.steps = []  # Steps for visualization

    def reset(self):
        """
        Reset the array to its original state and clear recorded steps.

        :return: The reset array.
        """
        self.array = self.original.copy()
        self.steps = []
        return self.array

    def _record_step(self):
        """
        Record the current state of the array for visualization.
        """
        self.steps.append(self.array.copy())

    def get_steps(self):
        """
        Get all recorded steps of the sorting process.

        :return: List of recorded steps.
        """
        return self.steps

    def bubble_sort(self, array=None):
        """
        Perform Bubble Sort on the array.

        :param array: Optional array to sort. If not provided, the initialized array is used.
        :return: Tuple containing the sorted array and the recorded steps.
        """
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()

        self._record_step()
        n = len(self.array)

        for i in range(n):
            for j in range(0, n-i-1):
                if self.array[j] > self.array[j+1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    self._record_step()

        return self.array, self.steps

    def selection_sort(self, array=None):
        """
        Perform Selection Sort on the array.

        :param array: Optional array to sort. If not provided, the initialized array is used.
        :return: Tuple containing the sorted array and the recorded steps.
        """
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()

        self._record_step()
        n = len(self.array)

        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j

            if min_idx != i:
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self._record_step()

        return self.array, self.steps

    def insertion_sort(self, array=None):
        """
        Perform Insertion Sort on the array.

        :param array: Optional array to sort. If not provided, the initialized array is used.
        :return: Tuple containing the sorted array and the recorded steps.
        """
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()

        self._record_step()
        n = len(self.array)

        for i in range(1, n):
            key = self.array[i]
            j = i-1
            while j >= 0 and key < self.array[j]:
                self.array[j+1] = self.array[j]
                j -= 1
            self.array[j+1] = key
            self._record_step()

        return self.array, self.steps

    def quick_sort(self, array=None):
        """
        Perform Quick Sort on the array.

        :param array: Optional array to sort. If not provided, the initialized array is used.
        :return: Tuple containing the sorted array and the recorded steps.
        """
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()

        def _quick_sort(low, high):
            if low < high:
                pi = _partition(low, high)
                _quick_sort(low, pi - 1)
                _quick_sort(pi + 1, high)

        def _partition(low, high):
            pivot = self.array[high]
            i = low - 1
            for j in range(low, high):
                if self.array[j] < pivot:
                    i += 1
                    self.array[i], self.array[j] = self.array[j], self.array[i]
                    self._record_step()
            self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
            self._record_step()
            return i + 1

        _quick_sort(0, len(self.array) - 1)
        return self.array, self.steps

    def merge_sort(self, array=None):
        """
        Perform Merge Sort on the array.

        :param array: Optional array to sort. If not provided, the initialized array is used.
        :return: Tuple containing the sorted array and the recorded steps.
        """
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()

        def _merge_sort(arr):
            if len(arr) > 1:
                mid = len(arr) // 2
                L = arr[:mid]
                R = arr[mid:]

                _merge_sort(L)
                _merge_sort(R)

                i = j = k = 0

                while i < len(L) and j < len(R):
                    if L[i] < R[j]:
                        arr[k] = L[i]
                        i += 1
                    else:
                        arr[k] = R[j]
                        j += 1
                    k += 1
                    self._record_step()

                while i < len(L):
                    arr[k] = L[i]
                    i += 1
                    k += 1
                    self._record_step()

                while j < len(R):
                    arr[k] = R[j]
                    j += 1
                    k += 1
                    self._record_step()

        _merge_sort(self.array)
        return self.array, self.steps

    def heap_sort(self, array=None):
        """
        Perform Heap Sort on the array.

        :param array: Optional array to sort. If not provided, the initialized array is used.
        :return: Tuple containing the sorted array and the recorded steps.
        """
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()

        def heapify(n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2

            if l < n and self.array[l] > self.array[largest]:
                largest = l

            if r < n and self.array[r] > self.array[largest]:
                largest = r

            if largest != i:
                self.array[i], self.array[largest] = self.array[largest], self.array[i]
                self._record_step()
                heapify(n, largest)

        n = len(self.array)

        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)

        for i in range(n - 1, 0, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]
            self._record_step()
            heapify(i, 0)

        return self.array, self.steps

    def shell_sort(self, array=None):
        """
        Perform Shell Sort on the array.

        :param array: Optional array to sort. If not provided, the initialized array is used.
        :return: Tuple containing the sorted array and the recorded steps.
        """
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()

        n = len(self.array)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = self.array[i]
                j = i
                while j >= gap and self.array[j - gap] > temp:
                    self.array[j] = self.array[j - gap]
                    j -= gap
                    self._record_step()
                self.array[j] = temp
                self._record_step()
            gap //= 2

        return self.array, self.steps

    def radix_sort(self, array=None):
        """
        Perform Radix Sort on the array.

        :param array: Optional array to sort. If not provided, the initialized array is used.
        :return: Tuple containing the sorted array and the recorded steps.
        """
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()

        def counting_sort(exp):
            n = len(self.array)
            output = [0] * n
            count = [0] * 10

            for i in range(n):
                index = (self.array[i] // exp) % 10
                count[index] += 1

            for i in range(1, 10):
                count[i] += count[i - 1]

            i = n - 1
            while i >= 0:
                index = (self.array[i] // exp) % 10
                output[count[index] - 1] = self.array[i]
                count[index] -= 1
                i -= 1

            for i in range(n):
                self.array[i] = output[i]
                self._record_step()

        max_val = max(self.array)
        exp = 1
        while max_val // exp > 0:
            counting_sort(exp)
            exp *= 10

        return self.array, self.steps


class DoublyLinkedList:
    """
    A class to represent a doubly linked list with basic operations.
    """

    class Node:
        """
        A class to represent a node in the doubly linked list.
        """

        def __init__(self, data):
            """
            Initialize a node with data.

            :param data: The data to store in the node.
            """
            self.data = data
            self.next = None
            self.prev = None

    def __init__(self):
        """
        Initialize an empty doubly linked list.
        """
        self.head = None

    def append(self, data):
        """
        Append an element to the end of the list.

        :param data: The data to append.
        """
        new_node = self.Node(data)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def prepend(self, data):
        """
        Prepend an element to the beginning of the list.

        :param data: The data to prepend.
        """
        self.append(data)
        self.head = self.head.prev

    def delete(self, data):
        """
        Delete an element from the list.

        :param data: The data to delete.
        """
        if not self.head:
            return

        current = self.head
        while True:
            if current.data == data:
                if current.next == current:  # Only one element in the list
                    self.head = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    if current == self.head:
                        self.head = current.next
                return
            current = current.next
            if current == self.head:
                break

    def display(self):
        """
        Display all elements in the list.

        :return: List of elements in the doubly linked list.
        """
        elements = []
        if not self.head:
            return elements

        current = self.head
        while True:
            elements.append(current.data)
            current = current.next
            if current == self.head:
                break
        return elements

    def search(self, data):
        """
        Search for an element in the list.

        :param data: The data to search for.
        :return: True if the element is found, False otherwise.
        """
        if not self.head:
            return False

        current = self.head
        while True:
            if current.data == data:
                return True
            current = current.next
            if current == self.head:
                break
        return False


class DEA:
    """
    A class to represent a deterministic finite automaton (DEA).
    """

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        """
        Initialize the DEA.

        :param states: Set of states.
        :param alphabet: Set of input symbols.
        :param transition_function: Transition function as a dictionary.
        :param start_state: The start state.
        :param accept_states: Set of accepting states.
        """
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        """
        Check if the DEA accepts the given input string.

        :param input_string: The input string to check.
        :return: True if the input is accepted, False otherwise.
        """
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            current_state = self.transition_function.get((current_state, symbol))
            if current_state is None:
                return False
        return current_state in self.accept_states


class Pushdown:
    """
    A class to represent a pushdown automaton (PDA).
    """

    def __init__(self, states, alphabet, stack_alphabet, transition_function, start_state, start_stack_symbol, accept_states):
        """
        Initialize the PDA.

        :param states: Set of states.
        :param alphabet: Set of input symbols.
        :param stack_alphabet: Set of stack symbols.
        :param transition_function: Transition function as a dictionary.
        :param start_state: The start state.
        :param start_stack_symbol: The initial stack symbol.
        :param accept_states: Set of accepting states.
        """
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.start_stack_symbol = start_stack_symbol
        self.accept_states = accept_states
        self.stack = [start_stack_symbol]

    def accepts(self, input_string):
        """
        Check if the PDA accepts the given input string.

        :param input_string: The input string to check.
        :return: True if the input is accepted, False otherwise.
        """
        current_state = self.start_state
        self.stack = [self.start_stack_symbol]  # Reset the stack for each run

        for symbol in input_string:
            if symbol not in self.alphabet:
                return False

            stack_top = self.stack.pop() if self.stack else None
            transition = self.transition_function.get((current_state, symbol, stack_top))

            if transition is None:
                return False

            current_state, stack_action = transition

            if stack_action is not None:
                for action in reversed(stack_action):
                    if action != '':
                        self.stack.append(action)

        # Check if the current state is an accept state and the stack is empty
        while self.stack:
            stack_top = self.stack.pop()
            transition = self.transition_function.get((current_state, '', stack_top))
            if transition is None:
                return False
            current_state, stack_action = transition
            if stack_action is not None:
                for action in reversed(stack_action):
                    if action != '':
                        self.stack.append(action)

        return current_state in self.accept_states and not self.stack

