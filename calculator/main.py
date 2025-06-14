import sys
from pkg.calculator import Calculator
from pkg.render import render

def main():
    if len(sys.argv) <= 1:
        print('Calculator app')
        print('Usage: python3 main.py "<expression>"')
        print('Example: python3 main.py "3 + 5"')
    else:
        calculator = Calculator()
        expression = ' '.join(sys.argv[1:])
        try:
            result = calculator.evaluate(expression)
            to_print = render(expression, result)
            print(to_print)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    main()