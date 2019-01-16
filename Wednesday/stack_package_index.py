# from algorithm import FileUtils
from thu.field import FieldLoader

# step1
# 根据两个堆栈信息的包名计算重合率和是否为包含关系
## 如果不为包含关系，且重合率较低，则直接判断该两个 stack 没毛线关系
## 否则进入 step2
class StackPackageIndex:
  def __init__(self):
    self.fieldLoader = FieldLoader()
    self.weights = [41, 37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2, 1]

  # 判断是否为包含关系，暂时判断为 item deep 全等，list size 可不同
  def contains(self, field1, field2):
    if len(field1) == 0 or len(field2) == 0: return False
    deep1 = len(field1[0])
    deep2 = len(field2[0])
    if deep1 != deep2: return False
    # list_length = len(field1) if len(field1) < len(field2) else len(field2)
    # deep_length = deep1 # xx if deep1 < deep2 else deep2
    def is_in(_field1, _field2):
      for i in range(0, len(_field1)):
        if _field1[i] not in _field2:
          return False
      return True
    # field1 in field2?
    # field2 in field1?
    return is_in(field1, field2) or is_in(field2, field1)

  def field_index(self, field1, field2):
    # 计算重合指数
    if len(field1) == 0 or len(field2) == 0: return 0.0
    if field1 == field2: return 1.0
    deep1 = len(field1[0])
    deep2 = len(field2[0])
    # 取 短领域 匹配
    list_length = len(field1) if len(field1) < len(field2) else len(field2)
    deep_length = deep1 if deep1 < deep2 else deep2
    score_weight = self.weights[0-deep_length:]
    # print(score_weight)
    # print(field1)
    # print(field2)
    total_count = 0
    right_count = 0
    for i in range(0, list_length):
      for j in range(0, deep_length):
        total_count += score_weight[j]
        if field1[i][j] == field2[i][j]:
          right_count += score_weight[j]
    return 0.0 if total_count == 0 else right_count/total_count

  def calculate(self, report_id1, report_id2):
    field1 = self.fieldLoader.load_field(report_id1)
    field2 = self.fieldLoader.load_field(report_id2)
    index = self.field_index(field1[0], field2[0])
    is_contain = self.contains(field1[0], field2[0])
    return {
      'is_contain': is_contain, # 是否包含关系
      'dup_index': index  # 不论是否包含，计算重合率
    }

# def main():
#   print('stack package tree start')
#   result = StackPackageIndex().calculate(450177, 450180)
#   print(result)

# main()