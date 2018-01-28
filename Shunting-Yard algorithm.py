class RPN:
    def __init__(self, string):
        self.string = string

    def Convert(self):
        self.converted = self.convertToRPN(self.splitIntoTokens())
        #if 'Error' in self.converted:
           # print "Conversion not possible"
        return self.converted

    def Evaluate(self):
        outputstack = []
        for token in self.converted:
            #self.printlist(outputstack)
            if self.TokenType(token) == 'Number':
                outputstack.append(token)
            else:
                if len(outputstack) > 1:
                    arg2 = outputstack.pop()
                    arg1 = outputstack.pop()
                    if token == '+':
                        outputstack.append(self.add(arg1, arg2))
                    elif token == '-':
                        outputstack.append(self.sub(arg1, arg2))
                    elif token == "*":
                        outputstack.append(self.multi(arg1, arg2))
                    elif token == '/':
                        outputstack.append(self.div(arg1, arg2))
                    elif token == '^':
                        outputstack.append(self.pow(arg1, arg2))
            #print('')
        return outputstack[0]

    def add(self, a, b):
        return float(a) + float(b)
    def sub(self, a, b):
        return float(a) - float(b)
    def multi(self, a, b):
        return float(a) * float(b)
    def div(self, a, b):
        if b != 0:
            return float(a)/float(b)
        else:
            return 'Error, can\'t divide by 0'
    def pow(self, a, b):
        return pow(float(a),float(b))


    def convertToRPN(self, input):
        #input received from splitIntoTokens, expected array of tokens (numbers and operators
        outputstack = []
        operatorstack = []
        for token in input:
            if self.TokenType(token) == 'Number':
                outputstack.append(token)
            elif self.TokenType(token) == 'Operator':
                while len(operatorstack) > 0:
                    currentoperator = operatorstack.pop()
                    if (currentoperator != '(' and (self.order(currentoperator) < self.order(token)) or (
                        (self.order(currentoperator) == self.order(token)) and self.isLeftAssociative(currentoperator))):
                        outputstack.append(currentoperator)
                    else:
                        operatorstack.append(currentoperator)
                        break
                operatorstack.append(token)
            elif token == '(':
                operatorstack.append(token)
            elif token == ')':
                leftbracketstatus = 0
                while len(operatorstack) > 0:
                    currentoperator = operatorstack.pop()
                    if currentoperator == '(':
                        leftbracketstatus = 1
                        break
                    outputstack.append(currentoperator)
                if leftbracketstatus == 0:
                    return "Error, mismatched parentheses"

            #==============================print output=============
            #print('\nOutput:')
            #self.printlist(outputstack)
            #print('\nOperators:')
            #self.printlist(operatorstack)
        while len(operatorstack) > 0:
            currentoperator = operatorstack.pop()
            if currentoperator == "(" or currentoperator == ')':
                return "Error, mismatched parentheses"
            else:
                outputstack.append(currentoperator)
        return outputstack
    def printlist(self, list):
        for i in list:
            print(i, sep='', end='')
    def splitIntoTokens(self):
        #takes string and returns array of tokens (numbers and operators)
        temparray = []
        resultarray = []
        for symbol in self.string:
            if symbol.isdigit():
                temparray.append(symbol)
            else:
                if len(temparray)  != 0:
                    resultarray.append(''.join(str(o) for o in temparray))
                resultarray.append(symbol)
                temparray = []
        if len(temparray) != 0:
            resultarray.append(''.join(str(o) for o in temparray))
        return resultarray

    def TokenType(self, token):
        operators = ['+', '-', '*', '/', '^']
        if token in operators:
            return 'Operator'
        elif token == '(' or token == ')':
            return 'Bracket'
        else:
            return 'Number'
    def isLeftAssociative(self, operator):
        operators = ['+', '-', '*', '/']
        if operator in operators:
            return True
        return False
    def order(self, operator):
        if operator == '^':
            #maybe add root
            return 1
        elif operator == "*" or operator == '/':
            return 2
        elif operator == '+' or operator == '-':
            return 3

string = '3+4*2/(1-5)^2'
print('String:\n' + string)
x = RPN(string)
print('Converted:')
x.printlist(x.Convert())
print('\nevaluated: ')
print(x.Evaluate())