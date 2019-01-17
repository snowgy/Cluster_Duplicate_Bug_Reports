import json
import os

if __name__ == '__main__':
    f = open('tmp2.json', 'r')
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
        result.append(tmp)

    jsObj = json.dumps(result)
    fileObject = open('tmp3.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()