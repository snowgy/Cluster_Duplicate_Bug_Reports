from report_loader import ReportLoader
from field import FieldLoader
import json, os

# CALL_STACK_DIR = '../Wednesday/thu/demodata'
CALL_STACK_DIR = '../dataset/call_stack'

# 加载文件/处理文件相关格式
class CallStackLoader:
  # def convert_2_list(self, json_):
  def load_call_stack(self, id):
    call_stack_file = open(CALL_STACK_DIR + '/call_data-' + str(id) + '.json')
    return json.load(call_stack_file)


# 根据源数据和 field 分析出调用链关系
# 调用链分三组：all、outer、inner
class CallStackCreater:
  def __init__(self):
    self.reportLoader = ReportLoader()
    self.fieldLoader = FieldLoader()
    pass

  def save(self, id, call_stacks):
    with open(CALL_STACK_DIR + '/call_data-' + str(id) + '.json', 'w') as outfile:
      json.dump(call_stacks, outfile)
  
  def fetch_call_stacks(self, calls, start, end):
    result = []
    for i in range(1, len(calls)):
      if i < start or i > end: continue
      # print(i, end, start)
      last_call = calls[i - 1]
      curt_call = calls[i]
      if last_call['package'] == curt_call['package']:
        continue
      info = {
        'provider': last_call,
        'caller': curt_call
      }
      result.append(info)
    return result

  def start(self, id):
    report = self.reportLoader.load_report(id)
    fields = self.fieldLoader.load_field(id)
    stack_arrs = report['stack_arr']
    result = []
    for i in range(0, len(stack_arrs)):
      current_field = fields[i]
      start = current_field['interest_start']
      end = current_field['interest_end']
      call_stack_src = stack_arrs[i]['calls']
      call_stack2 = self.fetch_call_stacks(call_stack_src, 0, start)
      call_stack3 = self.fetch_call_stacks(call_stack_src, end, len(call_stack_src))
      call_stack4 = self.fetch_call_stacks(call_stack_src, 0, len(call_stack_src))
      call_stack5 = self.fetch_call_stacks(call_stack_src, start - 1 if start > 0 else 0, end + 1)
      calls = {
        'exception': stack_arrs[i]['exception'],
        'inner': call_stack5,
        'outer_pre': call_stack2,
        'outer_suf': call_stack3,
        'all': call_stack4
      }
      result.append(calls)
    self.save(id, result)
    # print('Done!')

## 执行处理脚本
# def main():
#   print('Start...')
#   callStack = CallStackCreater()
#   # callStack.start(450132)

#   reportLoader = ReportLoader()
#   ids = reportLoader.load_id_from_dir()
#   print('Total ids: ', len(ids))
#   for id in ids:
#     # print('current: ', id)
#     callStack.start(id)
#   print('Done!')
#   # print(FieldLoader().load_field(450177))

# main()