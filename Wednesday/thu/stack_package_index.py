# from algorithm import FileUtils

# step1
# 根据两个堆栈信息的包名计算重合率和是否为包含关系
## 如果不为包含关系，且重合率较低，则直接判断该两个 stack 没毛线关系
## 否则进入 step2
class StackPackageIndex:
  def __init__(self):
    self.weights = [41, 37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2, 1]

  # 获取 package 列表, return ->[[org, eclipse, xxx, yyy], ...]
  def fetch_packages(self, stack_calls):
    packages = []
    for call_item in stack_calls:
      # print(call_item)
      packages.append(call_item['package'].split("."))
    return packages


  ## 获取该 stack calls 所在领域，如：
  # ['org', 'eclipse', 'swt']
  # ['org', 'eclipse', 'e4']
  # ['org', 'eclipse', 'core']
  # ['org', 'eclipse', 'ui']
  # ['org', 'eclipse', 'equinox']
  def fetch_field(self, packages):
    if len(packages) == 0: return []

    def remove_dups(list_):
      _list = []
      for item in list_:
        if item == None: continue
        if item not in _list:
          _list.append(item)
      return _list

    def fetch_at(list_, i):
      result = []
      for item in list_:
        value = item[i] if len(item) > i else None
        result.append(value)
      return remove_dups(result)

    def cal_deeps(list_): # 计算深度，找出区分领域包的位置
      _list = remove_dups(list_)
      current_deep = 0
      while(True):
        children = fetch_at(_list, current_deep)
        # print(current_deep, children)
        if len(children) > 2:
          return current_deep
        current_deep += 1

    def fetch_preffix_packages(list_, deep_length): # 提取包前缀，称为领域
      _list = remove_dups(list_)
      new_list = []
      for item in _list:
        _item = []
        length = deep_length + 1 if deep_length + 1 <= len(item) else len(item)
        for i in range(0, length):
          _item.append(item[i])
        new_list.append(_item)
      return remove_dups(new_list)

    deep_index = cal_deeps(packages)
    filed = fetch_preffix_packages(packages, deep_index)

    return filed

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
    return right_count/total_count

  def calculate(self, stack_arr1, stack_arr2):
    packages1 = self.fetch_packages(stack_arr1['calls'])
    packages2 = self.fetch_packages(stack_arr2['calls'])
    field1 = self.fetch_field(packages1)
    field2 = self.fetch_field(packages2)
    index = self.field_index(field1, field2)
    is_contain = self.contains(field1, field2)
    return {
      'is_contain': is_contain, # 是否包含关系
      'dup_index': index  # 不论是否包含，计算重合率
    }

# def main():
#   print('stack package tree start')
#   fileUtils = FileUtils()
#   report_test1 = fileUtils.load_report(450177)
#   report_test2 = fileUtils.load_report(450180)
#   result = StackPackageIndex().calculate(report_test1["stack_arr"][0], report_test2["stack_arr"][0])
#   print(result)

# main()