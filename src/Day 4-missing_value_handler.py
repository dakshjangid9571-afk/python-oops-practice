class MissingValueHandler:
    """Handle missing values in a numerical dataset."""

    def __init__(self, data):
                self.data = data

    def validate_input(self):
        """Validate the input dataset."""

        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if not self.data:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError("Dataset contains invalid values.")

    def find_missing_indexes(self):
        """Find the indexes of missing values."""
        missing_indexes = []

        for index, value in enumerate(self.data):
            if value is None:
                missing_indexes.append(index)

        return missing_indexes

    def count_missing_values(self):
        """Count the total number of missing values."""
        count = 0

        for value in self.data:
            if value is None:
                count += 1

        return count

    def calculate_mean(self):
        """Calculate the mean of available values."""
        total = 0
        count = 0

        for value in self.data:
            if value is not None:
                total += value
                count += 1

        if count == 0:
            raise ValueError("No valid values exist to calculate the mean.")

        return total / count

    def fill_missing_values(self):
        """Replace missing values with the mean."""
        mean = self.calculate_mean()
        self.cleaned_data = []

        for value in self.data:
            if value is None:
                self.cleaned_data.append(mean)
            else:
                self.cleaned_data.append(value)

        return self.cleaned_data

    def display_report(self):
        """Display the missing value analysis report."""
        cleaned_data = self.fill_missing_values()

        print("========================================")
        print("       MISSING VALUE REPORT")
        print("========================================")

        print(f"\nOriginal Data:")
        print(self.data)

        print(f"\nTotal Values       : {len(self.data)}")
        print(f"Missing Values     : {self.count_missing_values()}")
        print(f"Missing Indexes    : {self.find_missing_indexes()}")

        available_values = len(self.data) - self.count_missing_values()
        print(f"Available Values   : {available_values}")

        print(f"Mean               : {self.calculate_mean()}")

        print("\nCleaned Data:")
        print(cleaned_data)

        print("\n========================================")


def main():
    """Run the missing value handler."""
    data = [25, 30, None, 40, None, 35, 28]

    try:
        obj = MissingValueHandler(data)
        obj.validate_input()
        obj.display_report()
    except ValueError as error:
        print("Error:", error)

if __name__ == "__main__":
    main()                    