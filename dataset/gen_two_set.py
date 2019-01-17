import os

if __name__ == '__main__':
    f = open('true_data.txt', 'r')
    tmp1 = ''
    tmp2 = ''
    c = 0
    while 1:
        lines = f.readlines(100000)
        if not lines:
            break
        dev = lines.__len__()/5
        for line in lines:
            c+=1
            if c<dev:
                tmp1 += line
            else:
                tmp2 += line

    f1 = open('true_data_1.txt', 'w')
    f1.write(tmp1)
    f1.close()

    f2 = open('true_data_2.txt', 'w')
    f2.write(tmp2)
    f2.close()