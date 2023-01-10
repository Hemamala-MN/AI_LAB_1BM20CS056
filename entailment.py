combinations = [(True,True, True), (True,True,False),(True,False,True),(True,False, False),(False,True, True),(False,True, False),(False, False,True),(False,False, False)]
variable = {'p': 0,'q': 1, 'r': 2}		#In this program 3 variables(proposition symbols) are considered, they are assigned values 0,1,2
kb = ''				            #Knowledge base kb and query q are empty initially
q = ''
priority = {'~': 3, 'v': 1, '^': 2}		#3 Logical connectives are there and priorities are assigned to them

def input_rules():
    global kb, q			# Function to get input knowledge base and query(gloabal variables)
    kb = (input("Enter rule: "))
    q = input("Enter the Query: ")

def entailment():					#Entailment function
    global kb, q					#Starting part, just prinitng the truth table
    print('*'*10+"Truth Table Reference"+'*'*10)
    print('kb','alpha')
    print('*'*10)
    for comb in combinations:
        s = evaluatePostfix(toPostfix(kb), comb)		#Both knowledge base and query get their inputs in form of infix format.
        f = evaluatePostfix(toPostfix(q), comb)		#First we have to convert them to postfix using toPostfix function and input that and comb to evaluatePostfix function.
        print(s, f)					#Comb is 1 list (ex:(true,false,true) from combinations 2d-list , defined in the starting of program).
        print('-'*10)					#evaluatePostfix returns either true or false.
        if s and not f:
            return False
    return True

def isOperand(c):
    return c.isalpha() and c!='v'				#Function to check whether character in postfix is operand or not(example p,q,r the variables).
						#v is already used for "OR" logical connective . But, isalpha also considers v as alphabet. So, we remove v in isOperand function
def isLeftParanthesis(c):
    return c == '('					#Next 2 functions are used to check for left and right Parenthesis

def isRightParanthesis(c):
    return c == ')'

def isEmpty(stack):					#Checks whether stack is empty or not, return true if it is empty
    return len(stack) == 0

def peek(stack):
    return stack[-1]					#Used to get the top element of stack(Python allows negative indexing, -1 implies last element/ in stack it is top element)

def hasLessOrEqualPriority(c1, c2):
    try:
        return priority[c1]<=priority[c2]			#Function to check priority between two operators
    except KeyError:
        return False


def toPostfix(infix):
    stack = []					#Regular infix to postfix function
    postfix = ''
    for c in infix:
        if isOperand(c):
            postfix += c
        else:
            if isLeftParanthesis(c):
                stack.append(c)
            elif isRightParanthesis(c):
                operator = stack.pop()
                while not isLeftParanthesis(operator):
                    postfix += operator
                    operator = stack.pop()
            else:
                while (not isEmpty(stack)) and hasLessOrEqualPriority(c, peek(stack)):
                    postfix += stack.pop()
                stack.append(c)
    while (not isEmpty(stack)):
        postfix += stack.pop()

    return postfix

def evaluatePostfix(exp, comb):
    stack = []				#After infix to postfix , we take postfix and comb(that is comb from combinations such as (true,true,true) , etc. Empty stack taken initially
    for i in exp:
        if isOperand(i):				#If character is operand insert corresponding value of the particular combination in stack
            stack.append(comb[variable[i]])
        elif i == '~':
            val1 = stack.pop()			#If ~(NOT) is seen , element popped from stack and , complement inserted in stack
            stack.append(not val1)
        else:
            val1 = stack.pop()			#Otherwise in other logical operators. We take 2 operators and pass it to _eval function
            val2 = stack.pop()
            stack.append(_eval(i,val2,val1))
    return stack.pop()


def _eval(i, val1, val2):
    if i == '^':				#If AND(^) is there return and of 2 operators (python )
        return val2 and val1	      #If operator is not AND nor NOT, only OR is left and we return OR of two operands in that case.
    return val2 or val1


input_rules()
ans = entailment()
if ans:					#Testing function entailement returns bool value . Print accordingly
    print("The Knowledge Base entails query")
else:
    print("The Knowledge Base does not entail query")


