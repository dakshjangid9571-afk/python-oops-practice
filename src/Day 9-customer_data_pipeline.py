import os
import pandas as pd


class CustomerDataPipeline:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None
        self.summary = {}

    def validate_file(self):
        if not isinstance(self.file_path, str):
            raise TypeError("File path must be a string.")

        if not os.path.isfile(self.file_path):
            raise FileNotFoundError("CSV file does not exist.")

        if not self.file_path.lower().endswith(".csv"):
            raise ValueError("Only CSV files are supported.")

    def load_data(self):
        self.df = pd.read_csv(self.file_path)

        if self.df.empty:
            raise ValueError("Dataset is empty.")


    def validate_columns(self):
        required_columns = [
            "CustomerID",
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "Purchased"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in self.df.columns
        ]

        if missing_columns:
            raise KeyError(
                f"Required columns are missing: {missing_columns}"
            )

    def inspect_dataset(self):
        print("\n" + "=" * 50)
        print("           DATASET INSPECTION")
        print("=" * 50)

        print(f"Shape           : {self.df.shape}")
        print(f"Row Count       : {self.df.shape[0]}")
        print(f"Column Count    : {self.df.shape[1]}")
        print(f"Column Names    : {list(self.df.columns)}")

        print("\nData Types:")
        print(self.df.dtypes)

        print("\nMemory Information:")
        self.df.info()

    def generate_quality_report(self):
        total_rows = len(self.df)

        report = []

        for column in self.df.columns:
            missing_count = self.df[column].isnull().sum()
            missing_percentage = (missing_count / total_rows) * 100
            unique_values = self.df[column].nunique()

            report.append({
                "Column": column,
                "Data Type": str(self.df[column].dtype),
                "Missing Count": missing_count,
                "Missing %": missing_percentage,
                "Unique Values": unique_values
            })

        quality_report = pd.DataFrame(report)

        print("\n" + "=" * 50)
        print("           DATA QUALITY REPORT")
        print("=" * 50)
        print(quality_report)

        return quality_report

    def find_duplicates(self):
        duplicate_count = self.df.duplicated().sum()

        print("\n" + "=" * 50)
        print("           DUPLICATE REPORT")
        print("=" * 50)
        print(f"Duplicate Records : {duplicate_count}")

        return duplicate_count


    def remove_duplicates(self):
        self.cleaned_df = self.df.drop_duplicates().copy()

        print("\n" + "=" * 50)
        print("       DUPLICATE REMOVAL")
        print("=" * 50)
        print(f"Original Rows : {len(self.df)}")
        print(f"Cleaned Rows  : {len(self.cleaned_df)}")
        print(f"Removed Rows  : {len(self.df) - len(self.cleaned_df)}")

        return self.cleaned_df    

    def handle_missing_values(self):
        numerical_columns = ["Age", "Income", "PurchaseAmount"]

        for column in numerical_columns:
            median_value = self.cleaned_df[column].median()
            self.cleaned_df[column] = self.cleaned_df[column].fillna(median_value)

        print("\n" + "=" * 50)
        print("       MISSING VALUE HANDLING")
        print("=" * 50)

        for column in numerical_columns:
            print(
                f"{column} missing values after imputation : "
                f"{self.cleaned_df[column].isnull().sum()}"
            )

    def validate_cleaned_data(self):
        if self.cleaned_df.isnull().sum().sum() > 0:
            raise ValueError("Cleaned data still contains missing values.")

        if self.cleaned_df.duplicated().sum() > 0:
            raise ValueError("Cleaned data still contains duplicate records.")

        expected_types = {
            "Age": "numeric",
            "Income": "numeric",
            "Experience": "numeric",
            "PurchaseAmount": "numeric",
            "Purchased": "numeric"
        }

        for column, data_type in expected_types.items():
            if not pd.api.types.is_numeric_dtype(self.cleaned_df[column]):
                raise TypeError(
                    f"{column} must contain numeric values."
                )

        if not self.cleaned_df["Purchased"].isin([0, 1]).all():
            raise ValueError("Purchased must contain only 0 or 1.")

        print("\n" + "=" * 50)
        print("       CLEANED DATA VALIDATION")
        print("=" * 50)
        print("No missing values   : Valid")
        print("No duplicates       : Valid")
        print("Data types          : Valid")
        print("Purchased values    : Valid")

    def detect_invalid_values(self):
        invalid_values = {}

        invalid_age = self.cleaned_df[self.cleaned_df["Age"] <= 0]
        invalid_income = self.cleaned_df[self.cleaned_df["Income"] < 0]
        invalid_experience = self.cleaned_df[self.cleaned_df["Experience"] < 0]
        invalid_purchase = self.cleaned_df[
            self.cleaned_df["PurchaseAmount"] < 0
        ]
        invalid_purchased = self.cleaned_df[
            ~self.cleaned_df["Purchased"].isin([0, 1])
        ]

        if not invalid_age.empty:
            invalid_values["Age"] = invalid_age

        if not invalid_income.empty:
            invalid_values["Income"] = invalid_income

        if not invalid_experience.empty:
            invalid_values["Experience"] = invalid_experience

        if not invalid_purchase.empty:
            invalid_values["PurchaseAmount"] = invalid_purchase

        if not invalid_purchased.empty:
            invalid_values["Purchased"] = invalid_purchased

        print("\n" + "=" * 50)
        print("       INVALID VALUE REPORT")
        print("=" * 50)

        if invalid_values:
            for column, values in invalid_values.items():
                print(f"\nInvalid values in {column}:")
                print(values)
        else:
            print("No invalid values detected.")

        return invalid_values

    def create_features(self):
        self.cleaned_df["IncomePerExperience"] = self.cleaned_df.apply(
            lambda row: (
                row["Income"] / row["Experience"]
                if row["Experience"] != 0
                else 0
            ),
            axis=1
        )

        def categorize_purchase(amount):
            if amount < 2000:
                return "Low"
            elif amount <= 5000:
                return "Medium"
            else:
                return "High"

        self.cleaned_df["PurchaseCategory"] = (
            self.cleaned_df["PurchaseAmount"].apply(categorize_purchase)
        )

        print("\n" + "=" * 50)
        print("       FEATURE ENGINEERING")
        print("=" * 50)
        print(
            self.cleaned_df[
                [
                    "CustomerID",
                    "IncomePerExperience",
                    "PurchaseCategory"
                ]
            ]
        )

    def create_age_group(self):
        def categorize_age(age):
            if age < 30:
                return "Young"
            elif age <= 40:
                return "Adult"
            else:
                return "Senior"

        self.cleaned_df["AgeGroup"] = self.cleaned_df["Age"].apply(
            categorize_age
        )

        print("\n" + "=" * 50)
        print("           AGE GROUP")
        print("=" * 50)
        print(self.cleaned_df[["CustomerID", "Age", "AgeGroup"]])


    def get_high_value_customers(self):
        high_value_customers = self.cleaned_df[
            self.cleaned_df["PurchaseAmount"] > 5000
        ]

        print("\n" + "=" * 50)
        print("       HIGH VALUE CUSTOMERS")
        print("=" * 50)
        print(high_value_customers)

        return high_value_customers


    def sort_by_purchase_amount(self):
        sorted_df = self.cleaned_df.sort_values(
            by="PurchaseAmount",
            ascending=False
        )

        print("\n" + "=" * 50)
        print("       SORTED BY PURCHASE AMOUNT")
        print("=" * 50)
        print(sorted_df)

        return sorted_df



    def calculate_statistics(self):
        columns = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "IncomePerExperience"
        ]

        statistics = self.cleaned_df[columns].agg(
            ["mean", "median", "min", "max", "std"]
        )

        print("\n" + "=" * 50)
        print("           STATISTICS")
        print("=" * 50)
        print(statistics)

        return statistics


    def calculate_correlation(self):
        columns = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "Purchased"
        ]

        correlation = self.cleaned_df[columns].corr()

        print("\n" + "=" * 50)
        print("           CORRELATION")
        print("=" * 50)
        print(correlation)

        return correlation


    def analyze_by_purchase_status(self):
        grouped_analysis = self.cleaned_df.groupby("Purchased").agg(
            CustomerCount=("CustomerID", "count"),
            AverageAge=("Age", "mean"),
            AverageIncome=("Income", "mean"),
            AveragePurchaseAmount=("PurchaseAmount", "mean")
        )

        print("\n" + "=" * 50)
        print("       PURCHASE STATUS ANALYSIS")
        print("=" * 50)
        print(grouped_analysis)

        return grouped_analysis

    def perform_eda(self):
        total_customers = len(self.cleaned_df)
        average_age = self.cleaned_df["Age"].mean()
        average_income = self.cleaned_df["Income"].mean()
        median_income = self.cleaned_df["Income"].median()
        highest_purchase = self.cleaned_df["PurchaseAmount"].max()
        average_purchase = self.cleaned_df["PurchaseAmount"].mean()

        purchasers = (self.cleaned_df["Purchased"] == 1).sum()
        non_purchasers = (self.cleaned_df["Purchased"] == 0).sum()

        most_common_age_group = self.cleaned_df["AgeGroup"].mode()[0]
        most_common_purchase_category = (
            self.cleaned_df["PurchaseCategory"].mode()[0]
        )

        self.summary = {
            "Total Customers": total_customers,
            "Average Age": average_age,
            "Average Income": average_income,
            "Median Income": median_income,
            "Highest Purchase": highest_purchase,
            "Average Purchase": average_purchase,
            "Purchasers": purchasers,
            "Non-Purchasers": non_purchasers,
            "Most Common Age Group": most_common_age_group,
            "Most Common Purchase Category": most_common_purchase_category
        }

        print("\n" + "=" * 50)
        print("              EDA SUMMARY")
        print("=" * 50)

        for key, value in self.summary.items():
            print(f"{key:<30}: {value}")

        return self.summary


    def export_clean_data(self):
        output_path = "output/cleaned_customer_data.csv"

        self.cleaned_df.to_csv(output_path, index=False)

        print("\n" + "=" * 50)
        print("          DATA EXPORT")
        print("=" * 50)
        print(f"Cleaned dataset exported to: {output_path}")

        return output_path

    def run_pipeline(self):
        self.validate_file()
        self.load_data()
        self.validate_columns()
        self.inspect_dataset()
        self.generate_quality_report()
        self.find_duplicates()
        self.remove_duplicates()
        self.handle_missing_values()
        self.validate_cleaned_data()
        self.detect_invalid_values()
        self.create_features()
        self.create_age_group()
        self.get_high_value_customers()
        self.sort_by_purchase_amount()
        self.calculate_statistics()
        self.perform_eda()
        self.calculate_correlation()
        self.analyze_by_purchase_status()
        self.export_clean_data()


def main():
    file_path = "data/customer_data.csv"

    try:
        pipeline = CustomerDataPipeline(file_path)
        pipeline.run_pipeline()
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
    



        