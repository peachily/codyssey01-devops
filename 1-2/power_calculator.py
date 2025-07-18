def main () :
  try:
    base = float(input("제곱하고 싶은 숫자를 입력하세요: "))
  except ValueError:
    print("Invalid number input")
    return

  try:
    exponent = int(input("제곱할 횟수를 정수로 입력하세요: "))
  except ValueError:
    print("Invalid exponent input")
    return
  
  result = 1
  if exponent >= 0:
    for _ in range(exponent):
      result = result*base
  else:
    for _ in range(abs(exponent)):
      result = result / base

  print(result)

if __name__ == "__main__":
    main()
