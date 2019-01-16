import json, os
from report_loader import ReportLoader

# FIELD_DIR = '../dataset/field_copy'
FIELD_DIR = '../dataset/field'

# 加载文件/处理文件相关格式
class FieldLoader:
  # def convert_2_list(self, json_):
  def load_field(self, id):
    fieldfile = open(FIELD_DIR + '/field_data-' + str(id) + '.json')
    return json.load(fieldfile)


class FieldCreater:
  def __init__(self):
    self.reportLoader = ReportLoader()

  def save(self, id, fields):
    with open(FIELD_DIR + '/field_data-' + str(id) + '.json', 'w') as outfile:
      json.dump(fields, outfile)
    
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
    filed = fetch_preffix_packages(packages, deep_index)
    # print('fetch_preffix_packages done')

    return filed

  def start(self, id):
    report = self.reportLoader.load_report(id)
    stack_arrs = report['stack_arr']
    result = []
    for i in range(0, len(stack_arrs)):
      stack_arr = stack_arrs[i]
      packages = self.fetch_packages(stack_arr['calls'])
      # print(packages)
      field = self.fetch_field(packages)
      result.append(field)
    self.save(id, result)


def main():
  print('Start...')
  fieldCreater = FieldCreater()
  reportLoader = ReportLoader()
  ids = reportLoader.load_id_from_dir()
  print('Total ids: ', len(ids))
  for id in ids:
    # print('current: ', id)
    fieldCreater.start(id)
  print('Done!')
  # print(FieldLoader().load_field(450177))

main()