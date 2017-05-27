import re
import sys

def edit_distance(s1, s2):
    s1 = re.split(' |\n|\t', s1)
    s1 = filter(None, s1)
    s2 = re.split(' |\n|\t', s2)
    s2 = filter(None, s2)
    s1 = ' '.join(s1)
    s2 = ' '.join(s2)
#    print s1
#    print s2

    l1 = len(s1)
    l2 = len(s2)
    lis =[l1,l2]
    l = max(lis, key=lambda x: int(x))
    if l2 == 0:
        return l1
    previous_row = xrange(l2 + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        flag = 0
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1],l2

def ocr_ans(user, ground):
    userfile = open(user, 'r')
    user_text = userfile.read()
    user_text = user_text.decode('utf-8')
    groundfile = open(ground, 'r')
    ground_text = groundfile.read()
    ground_text = ground_text.decode('utf-8')
    return edit_distance(user_text, ground_text)    

#print ocr_ans(sys.argv[1], sys.argv[2])

