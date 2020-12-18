#this is pretty well defined how it works in another branch

def table(title, text_line):
    text_line.insert(0, title)

    text_column = [[line[i] for line in text_line] for i in range(len(text_line[0]))]

    # gets the max lenght of all collumns, for spacing

    max_line = [len(max(line, key=len)) for line in text_column]
    string = ''

    for words in range(len(title)):
        string += '+'
        string += '-' * (max_line[words] + 2)

    string += '+\n'

    for words in range(len(title)):
        string += "| " + title[words] + " "
        size = max_line[words] - len(title[words])
        string += ' ' * size
    string += "|\n"

    for words in range(len(title)):
        string += '+'
        string += '-' * (max_line[words] + 2)
    string += '+\n'

    for i in range(len(text_line)):
        if i == 0:
            # jumps the title
            continue
        for j in range(len(text_column)):
            string += "| " + text_line[i][j] + " "
            size = max_line[j] - len(text_line[i][j])
            string += ' ' * size
        string += "|\n"

    for words in range(len(title)):
        string += '+'
        string += '-' * (max_line[words] + 2)
    string += '+\n'

    return string