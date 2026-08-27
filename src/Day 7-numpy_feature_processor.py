import numpy as np


class NumpyFeatureProcessor:
    """Process numerical data using NumPy."""

    def __init__(self, data):
        self.data = data
        self.array = None
        self.min_max_data = None
        self.standardized_data = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        if not all(isinstance(value, (int, float)) for value in self.data):
            raise ValueError("Dataset contains non-numeric values.")

    def convert_to_array(self):
        self.array = np.array(self.data)
        return self.array

    def get_array_info(self):
        print("\nNumPy Array:")
        print(self.array)
        print("\nData Type:", self.array.dtype)
        print("Dimensions:", self.array.ndim)
        print("Shape:", self.array.shape)
        print("Size:", self.array.size)

    def calculate_minimum(self):
        return np.min(self.array)

    def calculate_maximum(self):
        return np.max(self.array)

    def calculate_mean(self):
        return np.mean(self.array)

    def calculate_standard_deviation(self):
        return np.std(self.array)

    def min_max_scale(self):
        minimum = np.min(self.array)
        maximum = np.max(self.array)

        if maximum == minimum:
            raise ValueError(
                "Cannot perform Min-Max Scaling when all values are the same."
            )

        self.min_max_data = (self.array - minimum) / (maximum - minimum)
        return self.min_max_data

    def standardize(self):
        mean = np.mean(self.array)
        standard_deviation = np.std(self.array)

        if standard_deviation == 0:
            raise ValueError(
                "Cannot perform Z-Score Standardization when "
                "standard deviation is zero."
            )

        self.standardized_data = (
            (self.array - mean) / standard_deviation
        )

        return self.standardized_data

    def display_report(self):
        minimum = self.calculate_minimum()
        maximum = self.calculate_maximum()
        mean = self.calculate_mean()
        standard_deviation = self.calculate_standard_deviation()

        self.min_max_scale()
        self.standardize()

        print("\n" + "=" * 50)
        print("         NUMPY FEATURE PROCESSING REPORT")
        print("=" * 50)

        print("\nOriginal Data:")
        print(self.data)

        print("\nNumPy Array:")
        print(self.array)

        print("\nData Type:", self.array.dtype)
        print("Dimensions:", self.array.ndim)
        print("Shape:", self.array.shape)
        print("Size:", self.array.size)

        print("\nMinimum:", minimum)
        print("Maximum:", maximum)
        print("Mean:", mean)
        print("Standard Deviation:", round(standard_deviation, 4))

        print("\nMin-Max Scaled:")
        print(np.round(self.min_max_data, 4))

        print("\nZ-Score Standardized:")
        print(np.round(self.standardized_data, 4))

        print("\n" + "=" * 50)

    def compare_scaling_methods(self):
        print("\nComparison of Scaling Methods:")
        print("-" * 55)
        print(f"{'Original':<15}{'Min-Max':<15}{'Z-Score':<15}")
        print("-" * 55)

        for original, min_max, standardized in zip(
            self.array,
            self.min_max_data,
            self.standardized_data
        ):
            print(f"{original:<15}{min_max:<15.4f}{standardized:<15.4f}")

        print("-" * 55)


def main():
    data = [10, 20, 30, 40, 50]

    try:
        obj = NumpyFeatureProcessor(data)

        obj.validate_input()
        obj.convert_to_array()
        obj.display_report()
        obj.compare_scaling_methods()

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()