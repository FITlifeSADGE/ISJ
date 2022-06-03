#!/usr/bin/env python3
# Do souboru, nazvaného podle konvence isj_proj6_xnovak00.py, implementujte třídu Polynomial, která bude pracovat s polynomy reprezentovanými pomocí seznamů. Například 2x^3 - 3x + 1 bude  reprezentováno jako [1,-3,0,2] (seznam začíná nejnižším řádem, i když se polynomy většinou zapisují opačně).

# Instance třídy bude možné vytvářet několika různými způsoby:
# pol1 = Polynomial([1,-3,0,2])
# pol2 = Polynomial(1,-3,0,2)
# pol3 = Polynomial(x0=1,x3=2,x1=-3)

# Volání funkce print() vypíše polynom v obvyklém formátu:
# >>> print(pol2)
# 2x^3 - 3x + 1

# Bude možné porovnávat vektory porovnávat:
# >>> pol1 == pol2
# True

# Polynomy bude možné sčítat a umocňovat nezápornými celými čísly:
# >>> print(Polynomial(1,-3,0,2) + Polynomial(0, 2, 1))
# 2x^3 + x^2 - x + 1
# >>> print(Polynomial(-1, 1) ** 2)
# x^2 - 2x  + 1

# A budou fungovat metody derivative() - derivace a at_value() - hodnota polynomu pro zadané x - obě pouze vrací výsledek, nemění samotný polynom:
# >>> print(pol1.derivative())
# 6x^2 - 3
# >>> print(pol1.at_value(2))
# 11
# >>> print(pol1.at_value(2,3))
# 35
# (pokud jsou zadány 2 hodnoty, je výsledkem rozdíl mezi hodnotou at_value() druhého a prvního parametru - může sloužit pro výpočet určitého integrálu, ale ten nemá být implementován)

# Maximální hodnocení bude vyžadovat, abyste:
# - uvedli "shebang" jako v předchozích projektech
# - důsledně používali dokumentační řetězce a komentovali kód
# - nevypisovali žádné ladicí/testovací informace při běžném "import isj_proj6_xnovak00"
# - zajistili, že následující platí:

class Polynomial:
    def __init__(self, *args, **kwargs): #převzato ze stack overflow https://stackoverflow.com/questions/36528271/instances-of-class-polynomial
        if args and isinstance(args[0], list):  # Polynomial([1,-3,0,2])
            self.coeffs=args[0]
        elif args:  # Polynomial(1,-3,0,2)
            self.coeffs=args
        else:  # Polynomial(x0=1,x3=2­,x1=-3)
            self.coeffs=[kwargs.get(x, 0) for x in ('x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16')]

    def __str__(self):
        string = ''
        for i, x in reversed(list(enumerate(self.coeffs))): #from highest degree of Polynomial
            if x:
                if x > 0:
                    string += '+ ' #space for proper formatting
                if x < 0:
                    x = str(x).replace('-', '- ') #adding space for proper formatting
                if x != 1 and x != '- 1':
                    string += str(x)
                if x == '- 1':
                    string += '- ' #using - x instead of - 1x
                if i > 0:
                    string += 'x' 
                    if i == 1:
                        string += ' ' #space for proper formatting in case of 3x - 5, previous formatting was 3x- 5
                if i > 1:
                    string += '^' + str(i) + ' '
                if i == 0 and (x == 1 or x == '- 1'):
                    x = str(x).replace('- ', '')
                    string += str(x) #adding the last number of list
        string = string.rstrip(' ') #removing space from right side of final string
        return '0' if not string else string.lstrip('+ ') #removing + and space from left side of final string
    
    def __eq__(self, other):
        if str(self) == str(other): #if both polynomials represented as strings are equal, returns True
            return True
        else:
            return False
    
    def __add__(self, other):
        Polynom_list = []
        if len(self.coeffs) > len(other.coeffs):
            Polynom_list = [0]*len(self.coeffs)
        else:
            Polynom_list = [0]*len(other.coeffs) #creates empty list of certain size 
        for i in range(len(self.coeffs)):
            Polynom_list[i] = self.coeffs[i] #assigns values of the first Polynomial to list
        for i in range(len(other.coeffs)):
            Polynom_list[i] += other.coeffs[i] #adds values of the second Polynomial to values in list
        return Polynomial(Polynom_list)
    
    def __mul__(self, other):
        Polynom_list = [0] *(len(self.coeffs) + len(other.coeffs)) #creates empty list of certain size
        for i in range(len(self.coeffs)):
            for j in range(len(other.coeffs)):
                Polynom_list[i+j] += (self.coeffs[i] * other.coeffs[j]) #multiplies all coefficients
        return Polynomial(Polynom_list)
       
    def __pow__(self, power):
        if power < 0:
            raise ValueError('umocnit lze pouze nezápornými čísly') #if power is negative, return a ValueError
        result = Polynomial(1)
        for _ in range(power): #to the power 2 == multiply once, thus power - 1
            result *= self
        return result
    
    def derivative(self):
        Polynom_list = [0] * (len(self.coeffs)) #creates empty list of certain size
        for i in range(1, len(self.coeffs)):
            Polynom_list[i-1] = self.coeffs[i] * i #start at second lowest degree of polynomial, multiply it by its degree
        return Polynomial(Polynom_list)
    
    def at_value(self, x, y=0):
        result = 0
        if y != 0:  #if both x and y were given
            for i in range(len(self.coeffs)):
                result += self.coeffs[i] * (y**i)
                result -= self.coeffs[i] * (x**i)
        else:   #if only x was given
            for i in range(len(self.coeffs)):
                result += self.coeffs[i] * (x**i) #start at lowest degree of polynomial, calculates the value of all coefficients 
        return result
        
        

def test():
    assert str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
    assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial(x2=0)) == "0"
    assert str(Polynomial(x0=0)) == "0"
    assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2,0,3)
    assert Polynomial(x2=0) == Polynomial(x0=0)
    assert str(Polynomial(x0=1)+Polynomial(x1=1)) == "x + 1"
    assert str(Polynomial([-1,1,1,0])+Polynomial(1,-1,1)) == "2x^2"
    pol1 = Polynomial(x2=3, x0=1)
    pol2 = Polynomial(x1=1, x3=0)
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(Polynomial(x0=-1,x1=1)**1) == "x - 1"
    assert str(Polynomial(x0=-1,x1=1)**2) == "x^2 - 2x + 1"
    pol3 = Polynomial(x0=-1,x1=1)
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(Polynomial(x0=2).derivative()) == "0"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative()) == "6x^2 + 3"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == "12x"
    pol4 = Polynomial(x3=2,x1=3,x0=2)
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert Polynomial(-2,3,4,-5).at_value(0) == -2
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3,5) == 44
    pol5 = Polynomial([1,0,-2])
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-1,3.6) == -23.92
    assert pol5.at_value(-1,3.6) == -23.92

if __name__ == '__main__':
    test()
    