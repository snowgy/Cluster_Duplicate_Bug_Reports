import json
from itertools import combinations

def equal(call1, call2):
    if call1["package"] == call2["package"] \
        and call1["class"] == call2["class"] \
        and call1["method"] == call2["method"]:
        return True
    return False

def is_same_stack(stack_1, stack_2):
    if stack_1["exception"] != stack_2['exception']:
        return False
    calls1 = stack_1["calls"]
    calls2 = stack_2["calls"]
    if len(calls1) != len(calls2):
        return False
    # 一一判断
    for i in range(0, len(calls1)):
        if not equal(calls1[i], calls2[i]):
            return False
    return True

# 结果：True：存在完全一致的堆栈
def is_same_report_withdiff(report_set0, report_set1):
    for stack_0 in report_set0["stack_arr"]:
        for stack_1 in report_set1["stack_arr"]:
            if is_same_stack(stack_0, stack_1):
                return True
    return False

def clean():
    f = open('../dataset/stack_data.json', 'r')
    data = json.load(f)
    reports = list(combinations(data, 2))
    for report_set in reports:
        if is_same_report_withdiff(report_set[0], report_set[1]):
            # 删掉其中一个
            pass

def main():
    pass







main()
