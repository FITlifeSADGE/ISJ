#!/usr/bin/env python3

# ukol za 2 body
def first_odd_or_even(numbers):
    """Returns 0 if there is the same number of even numbers and odd numbers
       in the input list of ints, or there are only odd or only even numbers.
       Returns the first odd number in the input list if the list has more even
       numbers.
       Returns the first even number in the input list if the list has more odd 
       numbers.

    >>> first_odd_or_even([2,4,2,3,6])
    3
    >>> first_odd_or_even([3,5,4])
    4
    >>> first_odd_or_even([2,4,3,5])
    0
    >>> first_odd_or_even([2,4])
    0
    >>> first_odd_or_even([3])
    0
    """
    even = 0
    odd = 0
    for number in numbers:
        if number % 2 == 0:
            even = even + 1
        else:
            odd = odd + 1
    if even == odd:
        return 0
    if even == len(numbers) or odd == len(numbers):
        return 0
    if even > odd:
        for number in numbers:
            if number % 2 != 0:
                return number
    else:
        for number in numbers:
            if number % 2 == 0:
                return number

# ukol za 3 body
def to_pilot_alpha(word):
    """Returns a list of pilot alpha codes corresponding to the input word

    >>> to_pilot_alpha('Smrz')
    ['Sierra', 'Mike', 'Romeo', 'Zulu']
    """

    pilot_alpha = ['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot',
        'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima', 'Mike',
        'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango',
        'Uniform', 'Victor', 'Whiskey', 'Xray', 'Yankee', 'Zulu']

    pilot_alpha_list = []
    num = 0
    for char in word:
        num = ord(char.upper())-ord('A')
        pilot_alpha_list.append(pilot_alpha[num])
     
    return pilot_alpha_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()