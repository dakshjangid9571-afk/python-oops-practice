import numpy as np


class NumpyDatasetAnalyzer:
    def __init__(self, data):
        self.data = data
        self.array = None


    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Dataset cannot be empty.")

        if not all(isinstance(row, list) for row in self.data):
            raise ValueError("Each row must be a list.")

        column_count = len(self.data[0])

        if column_count == 0:
            raise ValueError("Rows cannot be empty.")

        if not all(len(row) == column_count for row in self.data):
            raise ValueError("All rows must contain the same number of columns.")

        if not all(
            isinstance(value, (int, float, np.number))
            for row in self.data
            for value in row
        ):
            raise ValueError("Dataset contains non-numeric values.")    


    def convert_to_array(self):
        self.array = np.array(self.data)    

    def get_dataset_info(self):
        print("\nDataset Information:")
        print("Rows:", self.array.shape[0])
        print("Columns:", self.array.shape[1])
        print("Dimensions:", self.array.ndim)
        print("Size:", self.array.size)
        print("Data Type:", self.array.dtype)



    def get_column(self, column_index):
        return self.array[:, column_index]


    def get_row(self, row_index):
        return self.array[row_index, :]        


    def calculate_column_mean(self):
        return np.mean(self.array, axis=0)


    def calculate_column_minimum(self):
        return np.min(self.array, axis=0)


    def calculate_column_maximum(self):
        return np.max(self.array, axis=0)


    def calculate_column_std(self):
        return np.std(self.array, axis=0)


    def scale_features(self):
        minimum = np.min(self.array, axis=0)
        maximum = np.max(self.array, axis=0)

        if np.any(maximum == minimum):
            raise ValueError("Cannot scale features because a feature has constant values.")

        return (self.array - minimum) / (maximum - minimum)

    def feature_summary(self):
        return {
            "mean": self.calculate_column_mean(),
            "minimum": self.calculate_column_minimum(),
            "maximum": self.calculate_column_maximum(),
            "standard_deviation": self.calculate_column_std()
        }

    def display_report(self):
        print("=" * 60)
        print("         NUMPY 2D DATASET ANALYSIS REPORT")
        print("=" * 60)

        print("\nOriginal Data:")
        print(self.data)

        print("\nNumPy Array:")
        print(self.array)

        self.get_dataset_info()

        print("\nColumn Mean:")
        print(self.calculate_column_mean())

        print("\nColumn Minimum:")
        print(self.calculate_column_minimum())

        print("\nColumn Maximum:")
        print(self.calculate_column_maximum())

        print("\nColumn Standard Deviation:")
        print(self.calculate_column_std())

        print("\nFeature-wise Min-Max Scaled:")
        print(self.scale_features())

        print("\nFeature Summary:")
        summary = self.feature_summary()

        print("Mean:", summary["mean"])
        print("Minimum:", summary["minimum"])
        print("Maximum:", summary["maximum"])
        print("Standard Deviation:", summary["standard_deviation"])

        print("=" * 60)


def main():
    data = [
        [25, 30000, 2],
        [30, 45000, 5],
        [35, 60000, 8],
        [40, 80000, 12],
        [45, 100000, 15]
    ]

    try:
        obj = NumpyDatasetAnalyzer(data)

        obj.validate_input()
        obj.convert_to_array()
        obj.display_report()

    except ValueError as error:
        print("Error:", error)

if __name__ == "__main__":
    main()


                                    