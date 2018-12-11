import json

f = open('../dataset/processed_reports/eclipse_new.json', 'r')
data = json.load(f)
n_grams = set()

# add all n-grams to n_grams
for report in data:
    # 1-gram
    for stack in report['stack_arr']:
        n_grams.add(stack['symbol'])
    # 2-gram
    for i in range(len(report['stack_arr']) - 1):
        n_grams.add(report['stack_arr'][i]["symbol"] + report['stack_arr'][i + 1]["symbol"])

    # 3-gram
    for i in range(len(report['stack_arr']) - 2):
        n_grams.add(report['stack_arr'][i]["symbol"]
                    + report['stack_arr'][i + 1]["symbol"]
                    + report['stack_arr'][i + 2]["symbol"])

# calculating tf-idf

