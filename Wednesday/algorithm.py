import json


def dung(stack_1, stack_2):
    global i_2, i_1
    if stack_1.exception != stack_2.exception:
        return False

    package_name = stack_1.traces[0].package
    for i_1 in range(len(stack_1.traces)):
        if stack_1.traces[i_1].package != package_name:
            break

    for i_2 in range(len(stack_2.traces)):
        if stack_2.traces[i_2].package != package_name:
            break

    if stack_1.traces[i_1 - 1] == stack_2.traces[i_2 - 1]:
        if stack_1.traces[i_1] == stack_2.traces[i_2]:
            return True

    return False


def main():
    f = open('../dataset/stack_data.json', 'r')
    data = json.load(f)

    for report in data:
        for i in range(len(report.stack)-1):
            for j in range(i+1, len(report.stack)):
                print(report.id + i + j + dung(report.stack[i], report.stack[j]))
