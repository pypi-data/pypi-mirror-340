class BinaryGraphSearch:

    def __init__(self, data):
        """Initialize with a sorted list."""
        if not self._is_sorted(data):
            raise ValueError("Input data must be sorted in non-decreasing order.")
        self.data = data

    def _is_sorted(self, data):
        """Check if the data is sorted in non-decreasing order."""
        return all(data[i] <= data[i + 1] for i in range(len(data) - 1))


    def _binary_search(self, data, target):
        """Helper function for binary search (recursive)."""
        left, right = 0, len(data) - 1
        while left <= right:
            mid = (left + right) // 2
            if data[mid] == target:
                return mid
            elif data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    def search(self, target):
        """Search for a target element in the sorted list."""
        return self._binary_search(self.data, target)


    def insert(self, value):
        """Insert value into the sorted list maintaining order."""
        left, right = 0, len(self.data) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.data[mid] == value:
                return
            elif self.data[mid] < value:
                left = mid + 1
            else:
                right = mid - 1
        self.data.insert(left, value)

    def inorder_traversal(self):
        """Return the sorted list (simulating in-order traversal)."""
        return self.data

    def __str__(self):
        return f"Sorted List: {self.data}"

