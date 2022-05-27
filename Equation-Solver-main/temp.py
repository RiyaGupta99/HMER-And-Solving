from textwrap import indent
from sympy import integrate, expand, solve, symbols, diff
from sympy.parsing.sympy_parser import parse_expr
from sympy.plotting import plot

def solveInt(integral,variable):
    try:
        exp = parse_expr(integral)
        sympy_variable= symbols(variable)
        result = str(integrate(exp,sympy_variable))
        return result
    except:
        print("invalid equation")

def expandEquation(s):
    exp = parse_expr(s)
    result = str(expand(exp))
    return result

def solveEq(eq):
    minus_file_reader = open("minus.txt","r")
    contents = minus_file_reader.read()
    minus_file_reader.close()
    indices_minus = contents.split('.')
    print(f"indices:{indices_minus}")
    final_str = ''
    i = 0
    while i < len(eq):
        if str(i) in indices_minus:
            final_str += '-'
        elif eq[i] == 'i' and eq[i+1] == 'n' and eq[i+2] == 't':
            #Solving integral and add the solved string
            i_temp = i
            while eq[i_temp]!='d':
                if eq[i_temp] in ['+','-','*', '/', '%', '^', '='] or i_temp == len(eq):
                    print("Invalid Integral equation.")
                    return 
                i_temp+=1
            variable = eq[i_temp+1]
            integral_to_be_solved = eq[i+3:i_temp]
            integral_eq = solveEq(integral_to_be_solved)
            solved = solveInt(integral_eq,variable)

            i = i_temp+1
            final_str += str(solved)
        
        elif eq[i] == 'd':
            #solving derivative equation
            i_temp = i + 1
            while eq[i_temp]!='d':
                if eq[i_temp] in ['+','-','*', '/', '%', '^', '='] or i_temp == len(eq):
                    print("Invalid Integral equation.")
                    return 
                i_temp+=1
            derivate_to_be_solved = eq[i+1:i_temp]
            derivate_eq = solveEq(derivate_to_be_solved)
            solved = diff(derivate_eq)

            i = i_temp+1
            final_str += str(solved)

        elif eq[i] in ['(',')','+','-','*', '/', '%', '^', '=',';']:
            final_str += eq[i]
        
        elif eq[i].isnumeric():
            i_temp = i 
            temp = '' + eq[i] 
            while (i_temp+1)<=(len(eq)-1) and eq[i_temp+1].isnumeric():
                temp+=eq[i_temp+1] 
                i_temp += 1 
            if not eq[i-1].isnumeric() and eq[i-1] not in ['+','-','*', '/', '%', '^', '='] and i != 0 and final_str not in ['+','-','*', '/', '%', '^', '=']:
                final_str += '**'
            final_str += temp
            i=i_temp
        
        elif not eq[i].isnumeric():
            if i == 0:
                final_str += eq[i]
                i+=1
                continue
            elif final_str[i-1] not in ['+','-','*', '/', '%', '^', '='] and eq[i-1].isnumeric():
                print(f"i-1:{final_str[i-1]}")
                final_str += '*'
            final_str += eq[i]   
        
        i+=1
    return final_str
        

def graphEq(equation):
    #res = parse_expr(equation)
    p1 = plot(equation,show=False)
    p1.save('graph.png')
