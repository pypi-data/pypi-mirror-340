from pyhunt import trace


@trace
def multiply(a, b):
    return a * b


@trace
def calculate(numbers):
    total = 0
    for num in range(0, 2):
        total += multiply(num, 2)
    return total


@trace
def process_data(data):
    processed = [x + 1 for x in data]
    result = calculate(processed)
    return result


@trace
def main():
    data = [1, 2, 3]
    final_result = process_data(data)
    return final_result


if __name__ == "__main__":
    output = main()
    print(f"Final output: {output}")
