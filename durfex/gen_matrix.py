import json


class Report:
    grams = []


f = open('../stack_data.json', 'r')
data = json.load(f)
n_grams = set()
reports = []
i = 0
# add all n-grams to n_grams

for report in data:
    tmp = Report()
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
    del tmp

n_grams_dict = {}
i = 0
for gram in n_grams:
    n_grams_dict.setdefault(gram, i)
    i = i + 1

matrix = []


# calculating tf-idf
for report in reports:
    tmp_mat = [0]*len(n_grams)
    for gram in report.grams:
        tmp_mat[n_grams_dict.get(gram)] = 1
    matrix.append(tmp_mat)
    del tmp_mat

print(matrix)
