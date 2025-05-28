my_list = ['Richard', 'Gray', 'Weightlifting', 'Westminster']

def my_info(my_list):
    """ A function that passes a list of my information """
    count = 0
    for value in my_list:
        count += 1
    return count


if __name__ == '__main__':
    print(my_info(my_list))

