import json
import os

if __name__ == '__main__':
    f = open('tmp.json', 'r')
    stks = json.load(f)
    f.close()
    for stk_id in stks:
        for dup_id in stks[stk_id]:
            try:
                stks[dup_id].append(stk_id)
            except:
                pass

    jsObj = json.dumps(stks)
    fileObject = open('tmp2.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()