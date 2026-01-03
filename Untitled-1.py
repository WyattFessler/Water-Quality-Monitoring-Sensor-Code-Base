print("multiply")

repeat = True

while True:
    x = int(input("give number"))
    y = int(input("give second number"))

    operator = input("add (-), subtract (+), multiply (x), divide (/)")
    if operator == "-":
        print(f"{x - y}")
    elif operator == "+":
        print(f"{x + y}")
    elif operator == "x":
        print(f"{x * y}")
    elif operator == "/":
        print(f"{x / y}")
    else:
        print("not valid input")

    prompt = input("again? (y/n)")
    if prompt == "y":
        print("here goes!")
    if prompt == "n":
        break