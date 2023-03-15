from random import choice

# LOAD FIlES ===========================================================================================================
file_location = 'resource/words'


def read_file(final_name: str):
    with open(f'{file_location}/{final_name}.txt', 'r') as file_obj:
        return_list = list()
        for line in file_obj.readlines():
            if not line.startswith('#'):
                return_list.append(line.strip())
        return return_list


adjective = read_file('adj')
form = read_file('form')
noun = read_file('noun')
philosophers = read_file('philosophers')
pre = read_file('pre')
suffix = read_file('suf')
verb = read_file('verb')


# FORM DECODE ==========================================================================================================
def decode_form():
    form_choice = choice(form)

    res = str()
    i = 0

    while i < len(form_choice):
        c = form_choice[i]

        if c == 'A':
            res += choice(adjective)
        elif c == 'N':
            res += choice(noun)
        elif c == 'P':
            res += choice(philosophers)
        elif c == 'R':
            res += choice(pre)
        elif c == 'V':
            res += choice(verb)
        elif c == 'S':
            res += choice(suffix)
        elif c == ' ':
            res += choice(' ')
        elif c == '(':
            close_idx = form_choice.index(')', i)
            res += form_choice[i + 1: close_idx]
            i = close_idx + 1
            continue

        i += 1

    return res


# INTERFACE ============================================================================================================
num = int(input('How many sentences?\n'))
for i in range(num):
    print(decode_form())
