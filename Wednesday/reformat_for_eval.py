import json
import os

def gen_1():
    path = "./result"
    # id1 id2 真实值 预测值
    files = os.listdir(path)
    t_result = {}
    p_result = {}
    for file in files:
        f = open(path + "/" + file)
        line = f.readline()
        p_dup = []
        t_dup = []
        tmp = line.split()
        tmpid = tmp[0]
        while line:
            tmp = line.split()
            if tmp[2] == 'TRUE':
                t_dup.append(tmp[1])
            if tmp[3] == 'TRUE':
                p_dup.append(tmp[1])
            line = f.readline()
        t_result.setdefault(tmpid, t_dup)
        p_result.setdefault(tmpid, p_dup)
        f.close()

    for i in range(2):
        for stk_id in t_result:
            for dup_id in t_result[stk_id]:
                try:
                    if stk_id not in t_result[dup_id]:
                        if dup_id != stk_id:
                            t_result[dup_id].append(stk_id)
                    for double_dup_id in t_result[dup_id]:
                        if double_dup_id not in t_result[stk_id]:
                            if stk_id != double_dup_id:
                                t_result[stk_id].append(double_dup_id)

                except:
                    pass

    jsObj = json.dumps(t_result)
    fileObject = open('./formatted_result/t_result.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()

    for i in range(2):
        for stk_id in p_result:
            for dup_id in p_result[stk_id]:
                try:
                    if stk_id not in p_result[dup_id]:
                        if dup_id != stk_id:
                            p_result[dup_id].append(stk_id)
                    for double_dup_id in p_result[dup_id]:
                        if double_dup_id not in p_result[stk_id]:
                            if stk_id != double_dup_id:
                                p_result[stk_id].append(double_dup_id)

                except:
                    pass

    jsObj = json.dumps(p_result)
    fileObject = open('./formatted_result/p_result.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()


def gen_2():
    f = open('./formatted_result/p_result.json', 'r')
    stks = json.load(f)
    f.close()
    result = []
    visited = set()
    for stk in stks:
        tmp = []
        if stk not in visited:
            tmp.append(stk)
            visited.add(stk)
            for dup_stk in stks[stk]:
                if dup_stk not in visited:
                    visited.add(dup_stk)
                    tmp.append(dup_stk)
        if tmp is not []:
            result.append(tmp)

    jsObj = json.dumps(result)
    fileObject = open('./formatted_result/p_result_2.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()

    f = open('./formatted_result/t_result.json', 'r')
    stks = json.load(f)
    f.close()
    result = []
    visited = set()
    for stk in stks:
        tmp = []
        if stk not in visited:
            tmp.append(stk)
            visited.add(stk)
            for dup_stk in stks[stk]:
                if dup_stk not in visited:
                    visited.add(dup_stk)
                    tmp.append(dup_stk)
        if tmp is not []:
            result.append(tmp)

    jsObj = json.dumps(result)
    fileObject = open('./formatted_result/t_result_2.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()


if __name__ == '__main__':
    gen_1()
    gen_2()