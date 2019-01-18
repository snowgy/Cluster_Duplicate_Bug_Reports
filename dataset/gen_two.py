import json
import os

if __name__ == '__main__':
    f = open('tmp.json', 'r')
    stks = json.load(f)
    f.close()
    for i in range(5):
        for stk_id in stks:
            for dup_id in stks[stk_id]:
                try:
                    if stk_id not in stks[dup_id]:
                        if dup_id != stk_id:
                            stks[dup_id].append(stk_id)
                    for double_dup_id in stks[dup_id]:
                        if double_dup_id not in stks[stk_id]:
                            if stk_id != double_dup_id:
                                stks[stk_id].append(double_dup_id)

                except:
                    pass



    jsObj = json.dumps(stks)
    fileObject = open('tmp2.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()