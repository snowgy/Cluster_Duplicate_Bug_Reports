import json, os
from report_loader import ReportLoader

FIELD_DIR = '../../dataset/field'

# 加载文件/处理文件相关格式
class FieldLoader:
  # def convert_2_list(self, json_):
  def load_field(self, id):
    fieldfile = open(FIELD_DIR + '/field_data-' + str(id) + '.json')
    return json.load(fieldfile)


class FieldCreater:
  def __init__(self):
    self.reportLoader = ReportLoader()
    self.fliter_package = [
        "dalvik.system",
        "java.lang",
        "sun",
        "android",
    ]

  def jump(self, package_name):
    for fliter_name in self.fliter_package:
      if package_name.startswith(fliter_name):
        return True
    return False

  def save(self, id, fields):
    with open(FIELD_DIR + '/field_data-' + str(id) + '.json', 'w') as outfile:
      json.dump(fields, outfile)
    
  ## 获取 package 列表, return ->[[org, eclipse, xxx, yyy], ...]
  def fetch_packages(self, stack_calls):
    packages = []
    for call_item in stack_calls:
      # print(call_item)
      pkg = call_item['package']
      if self.jump(pkg):
        continue
      packages.append(pkg.split("."))
    return packages


  ## 获取该 stack calls 所在领域，如：
  # [['org', 'eclipse', 'swt']
  # ['org', 'eclipse', 'e4']
  # ['org', 'eclipse', 'core']
  # ['org', 'eclipse', 'ui']
  # ['org', 'eclipse', 'equinox']]
  def fetch_field(self, packages):
    if len(packages) == 0:
      return {
        'field': [],
        'deep': 0
      }

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
        # print(_list)
        children = fetch_at(_list, current_deep)
        if len(children) == 0: # 说明到底了
          return current_deep
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
    # print('cal_deeps')
    deep_index = cal_deeps(packages)
    # print('cal_deeps done, fetch_preffix_packages')
    field = fetch_preffix_packages(packages, deep_index)
    # print('fetch_preffix_packages done')

    return {
      'field': field,
      'deep': deep_index + 1 # deep length, not index
    }

  ## 获取重心领域，如：org.eclipse.swt 及其连续覆盖长度
  def fetch_interest_area(self, field_deep, packages):
    if len(packages) == 0 or field_deep == 0:
      return {
        'package': None,
        'length': 0,
        'start_index': 0,
        'end_index': 0
      }
    target_package = []
    target_count = 0
    target_end_index = 0
    current_package = packages[0][:field_deep]
    current_count = 0
    for i in range(0, len(packages)):
      now = packages[i][:field_deep]
      if now == current_package:
        current_count += 1
      else:
        current_count = 1
        current_package = now
      # 与目标包进行判断
      if current_count > target_count:
        target_package = now
        target_count = current_count
        target_end_index = i
    return {
      'package': '.'.join(target_package), # 包名，最有可能为目标区域的包
      'length': target_count, # 包重复次数，也可理解为包内调用链次数
      'start_index': target_end_index - target_count + 1, # 区域开始角标
      'end_index': target_end_index # 区域结束角标
    }

  def start(self, id):
    report = self.reportLoader.load_report(id)
    stack_arrs = report['stack_arr']
    result = []
    for i in range(0, len(stack_arrs)):
      stack_arr = stack_arrs[i]
      packages = self.fetch_packages(stack_arr['calls'])
      # print(packages)
      field_info = self.fetch_field(packages)
      field_area = field_info['field']
      field_deep = field_info['deep']
      # print(field_info)
      interest = self.fetch_interest_area(field_deep, packages)
      field = {
        'field': field_area, # [[]...]
        'deep': field_deep, # 3
        'interest_field': interest['package'], # org.eclipse.swt
        'interest_length': interest['length'], # 38
        'interest_start': interest['start_index'], # 0
        'interest_end': interest['end_index'] # 37
      }
      # print(field)
      result.append(field)
    self.save(id, result)

## 执行处理脚本
# def main():
#   print('Start...')
#   fieldCreater = FieldCreater()
#   # fieldCreater.start(450132)

#   reportLoader = ReportLoader()
#   ids = reportLoader.load_id_from_dir()
#   print('Total ids: ', len(ids))
#   for id in ids:
#     # print('current: ', id)
#     fieldCreater.start(id)
#   print('Done!')
#   # print(FieldLoader().load_field(450177))

# main()