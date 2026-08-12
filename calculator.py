class Calculator:
    def __init__(self):
        self.history = []

    def add (self, num1 , num2):
        result = num1 + num2
        self.history.append(f"answer = {result}")
        return result

    def subtract (self, num1 , num2):
        result = num1 - num2
        self.history.append(f"answer = {result}")
        return result

    def multiply (self, num1 , num2):
        result = num1 * num2
        self.history.append(f"answer = {result}")
        return result

    def divide (self, num1 , num2):
        if num2 == "0":
            ZeroDivisionError("cannot be divided by zero")
        result = num1 / num2
        self.history.append(f"answer = {result}")
        return result
    def print_history(self):
        for entry in self.history:
            print(entry)

def main():
    calculator = Calculator()
    while True:
        print("1 : addition")
        print("2 : subtract")
        print("3 : mulitply")
        print("4 : division")
        print("5 : print history")
        print("6 : quit")
        choice = input("Enter your choice : ")
        if choice == "6":
            break 
        elif choice in ["1","2","3","4"]:
            num1 = float(input("Enter number 1 : "))
            num2 = float(input("Enter number 2 : "))
            if choice == "1":
                print(calculator.add(num1 , num2))
            elif choice == "2":
                print(calculator.subtract(num1 , num2))
            elif choice == "3":
                print(calculator.multiply(num1 , num2))
            elif choice == "4":
                try:
                    print(calculator.divide(num1 , num2))
                except ZeroDivisionError as e:
                    print(str(e))

        elif choice == "5":
            print(calculator.print_history())
        else :
            print("invalid choice choose again")

main()
