import csv, os

MIDDLE_RESULT_DIR = '../../dataset/middle_result'

class StarterCache:
  def __init__(self):
     pass
    
  def load_result(self, report_id1, report_id2):
    # key = str(report_id1) + '-' + str(report_id2)
    with open(MIDDLE_RESULT_DIR + '/starter_result_' + str(report_id1) + '.csv', 'r') as readFile:
      rows = csv.reader(readFile)
      lines = list(rows)
      for line in lines:
        if line[1] == report_id2:
          return line[2:]
        # key = str(line[0]) + '-' + str(line[1])
        # self.dataset.update({key: line[2:]})
    return [] # 11 个长度的数组
  
# demo:
cache = StarterCache()
result1 = cache.load_result(482737, 298316)
result2 = cache.load_result(482737, 456119)
print(result1)
print(result2)
# ~output:
# ['0', '0', '0.0', '0.14285714285714285', '0.3333333333333333', '0', '0.3333333333333333', '0', '0', '0', '0']
# ['0', '0', '0.0', '0.14285714285714285', '0.3333333333333333', '0', '0.07692307692307693', '0', '0', '0', '0']
