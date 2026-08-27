class FeatureScaler:
    """Scale numerical data using Min-Max Scaling."""

    def __init__(self, data):
        self.data = data

    def validate_input(self):
        """Validate the input dataset."""

        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if not self.data:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if not isinstance(value, (int, float)):
                raise ValueError("Dataset contains invalid values.")


    def find_minimum(self):
        """Find the minimum value in the dataset."""
        minimum = self.data[0]

        for value in self.data:
            if value < minimum:
                minimum = value

        return minimum  

    def find_maximum(self):
        """Find the maximum value in the dataset."""
        maximum = self.data[0]

        for value in self.data:
            if value > maximum:
                maximum = value

        return maximum 
    
    def scale_data(self):
        """Scale data using Min-Max Scaling."""
        minimum = self.find_minimum()
        maximum = self.find_maximum()

        if minimum == maximum:
            raise ValueError(
                "Cannot scale data because all values are identical.")

        self.scaled_data = []

        for value in self.data:
            scaled_value = (value - minimum) / (maximum - minimum)
            self.scaled_data.append(scaled_value)

        return self.scaled_data
    
    def display_report(self):
        """Display the feature scaling report."""
        scaled_data = self.scale_data()

        print("========================================")
        print("       FEATURE SCALING REPORT")
        print("========================================")

        print("\nOriginal Data :", self.data)

        print(f"\nMinimum       : {self.find_minimum()}")
        print(f"Maximum       : {self.find_maximum()}")

        print("\nScaled Data   :", scaled_data)

        print("\n========================================")


def main():
    """Run the feature scaler."""
    data = [10, 20, 30, 40, 50]

    try:
        obj = FeatureScaler(data)
        obj.validate_input()
        obj.display_report()
    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
    