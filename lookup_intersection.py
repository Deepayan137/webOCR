
def find_different_unicodes():
    with open('Sanskrit.txt', 'r') as file1:
        with open('Sanskrit_Bhagavad.txt', 'r') as file2:
            #different = set(file1).intersection(file2)
             same = set(file1).intersection(file2)
    #different.discard('\n')
    same.discard('\n')

    with open('same.txt', 'w') as file_out:
        for line in same:
            file_out.write(line)




def find_different():
    find_different_unicodes()
    file1 = open("same.txt", "r")
    file2 = open("Sanskrit_Bhagavad.txt", "r")
    file3 = open("results.txt", "w")
    diff=[]
    list1 = file1.readlines()
    list2 = file2.readlines()

    diff=list(set(list1).symmetric_difference(set(list2)))
    for i in range(len(diff)):
        file3.write(diff[i])
    return diff
find_different()

def remove_unicodes(unic,list1):
    print list1
    while unic in list1:
        list1.remove(unic)
    return list1


