import json
import math


class Report:
    grams = []


def tf_idf(_gram, _report, _reports):
    n = 0
    for something in _report.grams:
        if _gram == something:
            n = n + 1
    tf = n / len(_report.grams)

    m = 1
    for somereport in _reports:
        if somereport.grams.__contains__(_gram):
            m = m + 1

    return tf * math.log(len(_reports)/m)


f = open('../dataset/stack_data.json', 'r')
data = json.load(f)
n_grams = set()
reports = []
i = 0
# add all n-grams to n_grams

for report in data:
    tmp = Report()
    tmp.grams = []
    # 1-gram
    for stack in report['stack_arr']:
        n_grams.add(stack['symbol'])
        tmp.grams.append(stack['symbol'])

    # 2-gram
    for i in range(len(report['stack_arr']) - 1):
        n_grams.add(report['stack_arr'][i]["symbol"] + report['stack_arr'][i + 1]["symbol"])
        tmp.grams.append(report['stack_arr'][i]["symbol"] + report['stack_arr'][i + 1]["symbol"])

    # 3-gram
    for i in range(len(report['stack_arr']) - 2):
        n_grams.add(report['stack_arr'][i]["symbol"]
                    + report['stack_arr'][i + 1]["symbol"]
                    + report['stack_arr'][i + 2]["symbol"])
        tmp.grams.append(report['stack_arr'][i]["symbol"]
                         + report['stack_arr'][i + 1]["symbol"]
                         + report['stack_arr'][i + 2]["symbol"])

    reports.append(tmp)
    # print(tmp.grams)

n_grams_dict = {}
i = 0
for gram in n_grams:
    n_grams_dict.setdefault(gram, i)
    i = i + 1

matrix = []

# calculating tf-idf
for report in reports:
    tmp_mat = [0] * len(n_grams)
    for gram in report.grams:
        tmp_mat[n_grams_dict.get(gram)] = tf_idf(gram, report, reports)
    matrix.append(tmp_mat)

print(matrix)
