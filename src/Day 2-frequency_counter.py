class FrequencyCounter:
    def __init__(self, numbers):
        self.numbers = numbers

    def validate_input(self):
        if not isinstance(self.numbers, list):
            raise TypeError("Input must be a list.")

        if len(self.numbers) == 0:
            raise ValueError("Input list cannot be empty.")

    def count_frequency(self):
        frequency = {}

        for number in self.numbers:
            if number in frequency:
                frequency[number] += 1
            else:
                frequency[number] = 1

        return frequency

    def display_result(self):
        frequency = self.count_frequency()
        print("Frequency:", frequency)

def main():
    try:
        numbers =[1, 2, 2, 3, 1, 5, 4, 2, 5, 5]

        counter = FrequencyCounter(numbers)

        counter.validate_input()
        counter.display_result()

    except (TypeError, ValueError) as error:
        print("Error:", error)

if __name__ == "__main__":
    main()