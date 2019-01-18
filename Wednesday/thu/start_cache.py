import csv, os

MIDDLE_RESULT_DIR = '../../dataset/middle_result'

class StarterCache:
  def __init__(self):
    self.dataset = {}

    filenames = os.listdir(MIDDLE_RESULT_DIR)
    for filename in filenames:  # 遍历文件夹
      with open(MIDDLE_RESULT_DIR + '/' + filename, 'r') as readFile:
        rows = csv.reader(readFile)
        lines = list(rows)
        for line in lines:
          key = str(line[0]) + '-' + str(line[1])
          self.dataset.update({key: line[2:]})
    
  def load_result(self, report_id1, report_id2):
    key = str(report_id1) + '-' + str(report_id2)
    return self.dataset[key] # 11 个长度的数组
  
# demo:
cache = StarterCache()
result1 = cache.load_result(482737, 298316)
result2 = cache.load_result(482737, 456119)
print(result1)
print(result2)