import json
import os
import random

from itertools import combinations

if __name__ == '__main__':
    f = open('tmp3.json', 'r')
    stks = json.load(f)
    f.close()

    result = ''
    length = len(stks)
    # for duang in stks:
    #     for cmb in combinations(duang, 2):
    #         result += cmb[0] + ',' + cmb[1] + ',\n'

    for i in range(length - 1):
        for cmb in combinations(stks[i], 2):
            err = ''
            while err == '':
                try:
                    err = stks[random.randint(i + 1, length-1)][0]
                except:
                    continue
            result += cmb[0] + ',' + cmb[1] + ',' + err + ',\n'

    # print(result)
    # jsObj = json.dumps(result)
    # fileObject = open('id_rel_err.json', 'w')
    # fileObject.write(jsObj)
    # fileObject.close()

    f = open('true_data.txt', 'w')
    f.write(result)
    f.close()
