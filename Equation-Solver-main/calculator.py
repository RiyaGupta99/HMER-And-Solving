from sympy.abc import *
from sympy import integrate
from sympy import solve,symbols
from sympy.plotting import plot
from sympy.parsing.sympy_parser import parse_expr
from temp import solveEq, graphEq

def solve_meThis(string_):
    try:
        if ';' in string_:
            
            y = symbols('y')
            eq1 = string_.split(';')[0]
            eq2 = string_.split(';')[1]
            print(f"eq1:{eq1}, eq2:{eq2}")
            lhs1 = parse_expr(eq1.split('=')[0])
            lhs2 = parse_expr(eq2.split('=')[0])
            rhs1 = parse_expr(eq1.split('=')[1])
            rhs2 = parse_expr(eq2.split('=')[1])
            solution = solve([lhs1-rhs1,lhs2-rhs2])
            eq1_y = solve(lhs1-rhs1,y)
            eq2_y = solve(lhs2-rhs2,y)
            p_eq1 = plot(eq1_y[0],show=False)
            p_eq2 = plot(eq2_y[0],show=False)
            p_eq1.append(p_eq2[0])
            p_eq1.save("graph.png")

        elif '=' not in string_:
            lhs = parse_expr(string_)
            rhs = parse_expr('0')
            solution = solve(lhs-rhs)
            graphEq(lhs-rhs)
        else:
            lhs =  parse_expr(string_.split("=")[0])
            rhs =  parse_expr(string_.split("=")[1])
            solution = solve(lhs-rhs)
            graphEq(lhs-rhs)
        
        return solution
    except:
        print("invalid equation")

def solver(operation):
    def operate(fb, sb, op):
        result = 0
        if operator == '+':
            result = int(first_buffer) + int(second_buffer)
        elif operator == '-':
            result = int(first_buffer) - int(second_buffer)
        elif operator == 'x':
            result = int(first_buffer) * int(second_buffer)
        return result

    if not operation or not operation[0].isdigit():
        return -1

    operator = ''
    first_buffer = ''
    second_buffer = ''

    for i in range(len(operation)):
        if operation[i].isdigit():
            if len(second_buffer) == 0 and len(operator) == 0:
                first_buffer += operation[i]
            else:
                second_buffer += operation[i]
        else:
            if len(second_buffer) != 0:
                result = operate(first_buffer, second_buffer, operator)
                first_buffer = str(result)
                second_buffer = ''
            operator = operation[i]

    result = int(first_buffer)
    if len(second_buffer) != 0 and len(operator) != 0:
        result = operate(first_buffer, second_buffer, operator)

    return result

def calculate(operation):
    string = ''
    temp = string = str(operation)
    # if 'D' in string:
    #     string = string.replace('D', '0')
    # if 'G' in string:
    #     string = string.replace('G', '6')
    # if 'b' in string:
    #     string = string.replace('b', '6')
    # if 'B' in string:
    #     string = string.replace('B', '8')
    # if 'Z' in string:
    #     string = string.replace('Z', '2')
    # if 'S' in string:
    #     string = string.replace('S', '=')
    # if 't' in string:
    #     string = string.replace('t', '+')
    # if 'f' in string:
    #     string = string.replace('f', '7')
    # if 'M' in string:
    #     string = string.replace('M', '-')
    # if 'W' in string:
    #     string = string.replace('W', '-')
    if '=' not in string and 'J' not in string and 'S' not in string and 'd' not in string:
        if 'x' in string:
            string = string.replace('x', '*')
        if 'X' in string:
            string = string.replace('X', '*')
        return string, eval(string)

    #integral = False
    #operation = string
    #string = ''
    #if operation[0]=='J' or operation[0]=='S':
    #    integral=True
    #    dx = operation[-2:]
    #    variable = operation[-1]
    #    operation = operation[1:]
    #ptr=1
    #string = operation[ptr-1]
    #print(operation)
    #while ptr != len(operation):
    #    if operation[ptr] in ['+','-','*', '/', '%', '^', '=']:
    #        string += operation[ptr]
    #    elif operation[ptr].isnumeric():
    #        temp_ptr = ptr
    #        temp = '' + operation[ptr]
    #        while (temp_ptr+1)<=(len(operation)-1) and operation[temp_ptr+1].isnumeric():
    #            temp+=operation[temp_ptr+1]
    #            temp_ptr += 1
    #        if not operation[ptr-1].isnumeric() and operation[ptr-1] not in ['+','-','*', '/', '%', '^', '=']:
    #            string += '**'
    #        string += temp
    #        ptr=temp_ptr
    #    
    #    elif not operation[ptr].isnumeric():
    #        if operation[ptr]=='d':
    #            break
    #        if operation[ptr-1].isnumeric():
    #            string += '*'
    #        string += operation[ptr]   
    #    ptr+=1
   
    #print("HERE" + string)
    ## if '=' not in string:
    ##     return string, solver(string)
    #if integral==True:
    #    return string,solve_int(string,variable)
    #else:
    final_eq_string = solveEq(string)
    return final_eq_string, solve_meThis(final_eq_string)
    # string = ''
    # string += operation[0]
    # for ptr in range(1,len(operation)):
    #     # char = operation[ptr]
    #     if operation[ptr] in ['+','-','*', '/', '%', '^', '=']:
    #         string += operation[ptr]
    #     elif operation[ptr].isnumeric():
    #         temp_ptr = ptr
    #         temp = '' + operation[ptr]
    #         while operation[temp_ptr+1].isnumeric():
    #             temp+=operation[temp_ptr+1]
    #             temp_ptr += 1
    #         if not operation[ptr-1].isnumeric():
    #             string += '**'
            
    #         string += temp
    # print("String = " + string)
        
    

