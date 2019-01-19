import json, os

JSON_DIR = '../../../dataset/json'
JSON_DIR_ALL = '../../../dataset/all_datas/json'

def load_report(id):
  reportfile = open(JSON_DIR_ALL + '/stack_data-' + str(id) + '.json')
  return json.load(reportfile)

def load_id_from_dir(path=JSON_DIR_ALL):
  ids = []
  filenames = os.listdir(path)
  for filename in filenames:  # 遍历文件夹
    report_id = int(filename[11:-5])
    ids.append(report_id)
  return ids

def save_report(id, report):
  with open(JSON_DIR + '/stack_data-' + str(id) + '.json', 'w') as outfile:
    json.dump(report, outfile)

def is_empty(report):
  stack_arrs = report['stack_arr']
  if len(stack_arrs) == 0: return True
  # for i in range(0, len(stack_arrs)):
  #   stack = stack_arrs[i]
  #   calls = stack['calls']
  #   if len(calls) == 0:
  #     return True
  calls = stack_arrs[0]['calls']
  if len(calls) == 0: return True
  return False

def start():
  ids = load_id_from_dir()
  count = 0
  for id in ids:
    report = load_report(id)
    if not is_empty(report):
      print("save report: ", id)
      save_report(id, report)
      count += 1
  print("total count: ", count)

start()