import re

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero."
    return a / b

def evaluate_expression(expression):
    try:
        # 공백 제거하고 정규표현식으로 분해
        match = re.match(r'^(-?\d+\.?\d*)([+\-*/])(-?\d+\.?\d*)$', expression.replace(' ', ''))

        if not match:
            return "잘못된 입력 형식입니다. (예: 2 + 3 또는 2+3)"

        a_str, operator, b_str = match.groups()
        a = int(float(a_str))
        b = int(float(b_str))

        if operator == "+":
            return f"Result: {add(a, b)}"
        elif operator == "-":
            return f"Result: {subtract(a, b)}"
        elif operator == "*":
            return f"Result: {multiply(a, b)}"
        elif operator == "/":
            result = divide(a, b)
            if isinstance(result, str):
                return result
            return f"Result: {result}"
        else:
            return "Invalid operator."

    except ValueError:
        return "숫자를 정확히 입력해주세요."
    except Exception as e:
        return f"예상치 못한 오류 발생: {e}"

def standard_calculator():
    try:
        a = int(float(input("첫 번째 숫자를 입력하세요: ")))
        b = int(float(input("두 번째 숫자를 입력하세요: ")))
        operator = input("연산자를 입력하세요 (+, -, *, /): ")

        if operator == "+":
            print(f"Result: {add(a, b)}")
        elif operator == "-":
            print(f"Result: {subtract(a, b)}")
        elif operator == "*":
            print(f"Result: {multiply(a, b)}")
        elif operator == "/":
            result = divide(a, b)
            if isinstance(result, str):
                print(result)
            else:
                print(f"Result: {result}")
        else:
            print("Invalid operator.")
    except ValueError:
        print("숫자를 정확히 입력해주세요.")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")

if __name__ == "__main__":
    print("계산 방식 선택 (1: 숫자+연산자+숫자 형식 / 2: 순서대로 입력): ", end="")
    mode = input()

    if mode == "1":
        expr = input("Enter expression: ")
        print(evaluate_expression(expr))
    elif mode == "2":
        standard_calculator()
    else:
        print("잘못된 선택입니다. 1 또는 2를 입력하세요.")
