import csv

MIDDLE_RESULT_DIR = '../../dataset/middle_result'

class StarterCache:
  def __init__(self):
    self.dataset = {}
    with open('people.csv', 'r') as readFile:
      rows = csv.reader(readFile)
      lines = list(rows)
      for line in lines:
        key = str(line[0]) + '-' + str(line[1])
        self.dataset.update({key, line[2:]})
    

  def load_result(self, report_id1, report_id2):
    key = str(report_id1) + '-' + str(report_id2)
    return self.dataset[key] # 11 个长度的数组
  