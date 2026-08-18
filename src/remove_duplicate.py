class RemoveDuplicates:
    """A class to remove duplicate values from a list."""

    def __init__(self, numbers):
        """Initialize the object with the given list of numbers."""
        self.numbers = numbers

    def validate_input(self):
        """Validate that the input is a list."""
        if not isinstance(self.numbers, list):
            raise TypeError("Input must be a list.")

    def remove_duplicates(self):
        """Remove duplicate values from the list."""
        unique_numbers = []

        for value in self.numbers:
            if value not in unique_numbers:
                unique_numbers.append(value)

        return unique_numbers

    def display_result(self):
        """Display the original and unique lists."""
        unique_numbers = self.remove_duplicates()

        print("Original List :", self.numbers)
        print("Unique List   :", unique_numbers)


def main():
    numbers = [10, 20, 10, 30, 40, 20, 50, 30]

    try:
        obj = RemoveDuplicates(numbers)
        obj.validate_input()
        obj.display_result()

    except TypeError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()