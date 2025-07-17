try:
  number = float(input("제곱하고 싶은 숫자를 입력하세요: "))
except ValueError:
  print("Invalid number input")

try:
    exponent = int(input("제곱할 횟수를 정수로 입력하세요: "))
except ValueError:
   print("Invalid exponent input")

