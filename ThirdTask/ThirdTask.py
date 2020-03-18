def check_digit_groups(string):
    is_in_group = False
    number_of_groups = 0
    for i in range(1, len(string)):
        if string[i] == string[i-1]:
            if not is_in_group:
                is_in_group = True
                number_of_groups += 1
        else:
            is_in_group = False
    return number_of_groups >= 2


def check_digits_increasing(string):
    for i in range(1, len(string)):
        if string[i-1] > string[i]:
            return False
    return True


lowerCap = 372 ** 2
upperCap = 809 ** 2
counter = 0
for number in range(lowerCap, upperCap + 1):
    number_txt = str(number)
    if check_digits_increasing(number_txt):
        if check_digit_groups(number_txt):
            # print(number_txt)
            counter += 1
print("matching passwords: " + str(counter))




