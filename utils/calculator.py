def calculate(num1, operator, num2):
    if operator == "+":
        return num1 + num2

    elif operator == "-":
        return num1 - num2

    elif operator == "*":
        return num1 * num2

    elif operator == "/":
        if num2 == 0:
            raise ValueError("لا يمكن القسمة على صفر")
        return num1 / num2

    else:
        raise ValueError("عملية غير صحيحة")