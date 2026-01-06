def calculate_average(numbers):
    total = 0
    for number in numbers:
        total += number
    breakpoint() 
    average = total / len(numbers) 
    return average

data = [10, 20, 30, 40]
avg = calculate_average(data)
print(f"The average is: {avg}")