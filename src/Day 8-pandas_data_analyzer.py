import pandas as pd


class PandasDataAnalyzer:

    def __init__(self, data):
        self.data = data
        self.df = None
        self.cleaned_df = None

    def create_dataframe(self):
        self.df = pd.DataFrame(self.data)
        return self.df

    def validate_input(self):
        required_columns = ["Customer", "Age", "Income", "Experience", "Purchased"]

        if not isinstance(self.data, list) or len(self.data) == 0:
            raise ValueError("Input dataset must be a non-empty list.")

        if not all(isinstance(record, dict) for record in self.data):
            raise ValueError("Each record must be a dictionary.")

        first_columns = set(self.data[0].keys())

        for record in self.data:
            if set(record.keys()) != first_columns:
                raise ValueError("All records must have consistent columns.")

        missing_columns = [
            column for column in required_columns
            if column not in first_columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        return True
    
    def get_dataset_info(self):
        print("\nDataset Information:")
        print(f"Rows: {self.df.shape[0]}")
        print(f"Columns: {self.df.shape[1]}")
        print(f"Column Names: {list(self.df.columns)}")
        print("\nData Types:")
        print(self.df.dtypes)
        print(f"Shape: {self.df.shape}")

    def find_missing_values(self):
        return self.df.isnull()


    def count_missing_values(self):
        return self.df.isnull().sum()

    def find_duplicates(self):
        return self.df.duplicated().sum()

    def remove_duplicates(self):
        self.cleaned_df = self.df.drop_duplicates().copy()
        return self.cleaned_df

    def fill_missing_values(self):
        income_mean = self.cleaned_df["Income"].mean()
        self.cleaned_df["Income"] = self.cleaned_df["Income"].fillna(income_mean)
        return self.cleaned_df

    def filter_customers(self, min_income):
        return self.cleaned_df[self.cleaned_df["Income"] >= min_income]

    def sort_by_income(self, ascending=True):
        return self.cleaned_df.sort_values(
            by="Income",
            ascending=ascending
        )

    def calculate_statistics(self):
        numerical_columns = ["Age", "Income", "Experience", "Purchased"]

        statistics = {}

        for column in numerical_columns:
            statistics[column] = {
                "Mean": self.cleaned_df[column].mean(),
                "Minimum": self.cleaned_df[column].min(),
                "Maximum": self.cleaned_df[column].max(),
                "Std Dev": self.cleaned_df[column].std()
            }

        return statistics

    def analyze_features(self):
        features = ["Age", "Income", "Experience", "Purchased"]

        print("\nFeature Statistics:")

        for feature in features:
            print(f"\n{feature}:")
            print(f"Mean: {self.cleaned_df[feature].mean()}")
            print(f"Minimum: {self.cleaned_df[feature].min()}")
            print(f"Maximum: {self.cleaned_df[feature].max()}")
            print(f"Std Dev: {self.cleaned_df[feature].std()}")


    def analyze_target(self):
        purchased = (self.cleaned_df["Purchased"] == 1).sum()
        not_purchased = (self.cleaned_df["Purchased"] == 0).sum()

        print("\nPurchase Analysis:")
        print(f"Purchased: {purchased}")
        print(f"Not Purchased: {not_purchased}")

        return purchased, not_purchased

    def perform_eda(self):
        customer_count = len(self.cleaned_df)
        average_age = self.cleaned_df["Age"].mean()
        average_income = self.cleaned_df["Income"].mean()
        highest_income = self.cleaned_df["Income"].max()
        average_experience = self.cleaned_df["Experience"].mean()
        number_of_purchasers = (self.cleaned_df["Purchased"] == 1).sum()

        print("\nEDA Report:")
        print(f"Customer Count: {customer_count}")
        print(f"Average Age: {average_age}")
        print(f"Average Income: {average_income}")
        print(f"Highest Income: {highest_income}")
        print(f"Average Experience: {average_experience}")
        print(f"Number of Purchasers: {number_of_purchasers}")

        return {
            "Customer Count": customer_count,
            "Average Age": average_age,
            "Average Income": average_income,
            "Highest Income": highest_income,
            "Average Experience": average_experience,
            "Number of Purchasers": number_of_purchasers
        }

    def display_report(self):
        print("\n" + "=" * 50)
        print("CUSTOMER DATA ANALYSIS")
        print("=" * 50)

        print(f"\nOriginal Dataset Shape: {self.df.shape}")

        missing_values = self.count_missing_values()["Income"]
        duplicate_records = self.find_duplicates()

        print(f"Missing Income Values: {missing_values}")
        print(f"Duplicate Records: {duplicate_records}")
        print(f"Rows After Cleaning: {self.cleaned_df.shape[0]}")

        statistics = self.calculate_statistics()

        print("\nFeature Statistics:")

        for feature, values in statistics.items():
            print(
                f"{feature} - "
                f"Mean: {values['Mean']}, "
                f"Minimum: {values['Minimum']}, "
                f"Maximum: {values['Maximum']}, "
                f"Std Dev: {values['Std Dev']}"
            )

        purchased, not_purchased = self.analyze_target()

        

        self.perform_eda()


def main():
    data = [
    {"Customer": "C001", "Age": 25, "Income": 30000, "Experience": 2, "Purchased": 0},
    {"Customer": "C002", "Age": 30, "Income": 45000, "Experience": 5, "Purchased": 1},
    {"Customer": "C003", "Age": 35, "Income": None, "Experience": 8, "Purchased": 1},
    {"Customer": "C004", "Age": 40, "Income": 80000, "Experience": 12, "Purchased": 1},
    {"Customer": "C005", "Age": 45, "Income": 100000, "Experience": 15, "Purchased": 0},
    {"Customer": "C002", "Age": 30, "Income": 45000, "Experience": 5, "Purchased": 1}
]

    try:
        analyzer = PandasDataAnalyzer(data)

        analyzer.validate_input()
        analyzer.create_dataframe()
        analyzer.get_dataset_info()
        analyzer.find_missing_values()
        analyzer.count_missing_values()
        analyzer.find_duplicates()
        analyzer.remove_duplicates()
        analyzer.fill_missing_values()
        filtered_customers = analyzer.filter_customers(50000)
        sorted_customers = analyzer.sort_by_income()
        analyzer.calculate_statistics()
        analyzer.display_report()

    except (ValueError, KeyError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()

    
                                                    







