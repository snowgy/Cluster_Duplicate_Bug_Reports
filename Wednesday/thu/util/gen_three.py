import json
import os

if __name__ == '__main__':
    f = open('../steps/stack_dups_data.json', 'r')
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
        if tmp != []:
          result.append(tmp)

    jsObj = json.dumps(result)
    fileObject = open('real_buckets.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()