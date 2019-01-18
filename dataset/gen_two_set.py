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
                tmp2 += line[:-1] + ' '

    f1 = open('true_data_1.txt', 'w')
    f1.write(tmp1)
    f1.close()
    tmp3 = set()
    for i in tmp2.split(' '):
        tmp3.add(i)

    tmp4 = ''
    for i in tmp3:
        tmp4 += i + ' '

    print(tmp4)
    f4 = open('true_data_2.txt', 'w')
    f4.write(tmp4)
    f4.close()