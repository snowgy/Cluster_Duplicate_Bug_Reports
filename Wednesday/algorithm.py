import json
from itertools import combinations
from sklearn.metrics import classification_report


def dung(stack_1, stack_2):
    global i_2, i_1
    if stack_1["exception"] != stack_2['exception']:
        return False

    package_name = stack_1["calls"][0]["package"]
    for i_1 in range(len(stack_1["calls"])):
        if stack_1["calls"][i_1]["package"] != package_name:
            break

    for i_2 in range(len(stack_2["calls"])):
        if stack_2["calls"][i_2]["package"] != package_name:
            break

    if stack_1["calls"][i_1 - 1] == stack_2["calls"][i_2 - 1]:
        if stack_1["calls"][i_1] == stack_2["calls"][i_2]:
            return True

    return False


def diff(report_set):
    try:
        for stack_0 in report_set[0]["stack_arr"]:
            for stack_1 in report_set[1]["stack_arr"]:
                if dung(stack_0, stack_1):
                    return True
        return False
    except:
        # print(report_set[0]["stack_id"])
        return False

def to_list(dict_):
    list_ = []
    for v in dict_.values():
        list_.append(1 if v else 0)
    return list_

def main():
    f = open('../dataset/stack_data.json', 'r')
    data = json.load(f)
    reports = list(combinations(data, 2))
    result = {}
    id_result = {}
    for report_set in reports:
        val = str(report_set[0]["stack_id"]) + " " + str(report_set[1]["stack_id"])
        result.setdefault(val, diff(report_set))
        aaa = report_set[1]["stack_id"] in report_set[0]["duplicated_stack_id"]
        id_result.setdefault(val, aaa)

    print(len(result))
    print(len(id_result))
    y_true = to_list(id_result)
    y_pred = to_list(result)
    print(classification_report(y_true, y_pred))







main()
