class StatisticalAnalyzer:
    """Analyze numerical data using basic statistical calculations."""

    def __init__(self, numbers):
        self.numbers = numbers

    def validate_input(self):
        """Validate the input dataset."""

        if not isinstance(self.numbers, list):
            raise ValueError("Input must be a list.")    

        if not self.numbers:
            raise ValueError("Input list cannot be empty.")

        for value in self.numbers:
            if not isinstance(value, (int, float)):
                raise ValueError(
                    "Input must contain only numerical values."
                )

    def calculate_mean(self):
        """Calculate the mean of the dataset."""
        total = 0

        for value in self.numbers:
            total += value

        return total / len(self.numbers)

    def calculate_median(self):
        """Calculate the median of the dataset."""
        sorted_numbers = sorted(self.numbers)
        n = len(sorted_numbers)

        middle = n // 2

        if n % 2 == 1:
            return sorted_numbers[middle]

        return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2

    
    def calculate_mode(self):
        """Calculate the mode or modes of the dataset."""
        frequency = {}

        for value in self.numbers:
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1

        max_frequency = max(frequency.values())

        if max_frequency == 1:
            return "No unique mode"

        modes = []

        for value, count in frequency.items():
            if count == max_frequency:
                modes.append(value)

        return modes    


    def find_minimum(self):
        """Find the minimum value in the dataset."""
        minimum = self.numbers[0]

        for value in self.numbers:
            if value < minimum:
                minimum = value

        return minimum

    def find_maximum(self):
        """Find the maximum value in the dataset."""
        maximum = self.numbers[0]

        for value in self.numbers:
            if value > maximum:
                maximum = value

        return maximum

    def count_unique_values(self):
        """Count the number of unique values."""
        unique_values = []

        for value in self.numbers:
            if value not in unique_values:
                unique_values.append(value)

        return len(unique_values)

    def display_result(self):
        """Display the statistical analysis report."""
        print("================================")
        print("       STATISTICAL REPORT")
        print("================================")

        print(f"\nOriginal Data : {self.numbers}")
        print(f"\nMean          : {self.calculate_mean():.2f}")
        print(f"Median        : {self.calculate_median()}")
        mode = self.calculate_mode()

        if isinstance(mode, list) and len(mode) == 1:
            mode = mode[0]

        print(f"Mode          : {mode}")
        print(f"Minimum       : {self.find_minimum()}")
        print(f"Maximum       : {self.find_maximum()}")
        print(f"Unique Values : {self.count_unique_values()}")

        print("\n================================")

def main():
    """Run the statistical analyzer."""
    numbers = [10, 20, 20, 30, 40, 50]

    try:
        analyzer = StatisticalAnalyzer(numbers)
        analyzer.validate_input()
        analyzer.display_result()
    except ValueError as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
                