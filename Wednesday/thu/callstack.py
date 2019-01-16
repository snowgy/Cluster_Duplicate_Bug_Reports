from report_loader import ReportLoader
from field import FieldLoader
import json, os

CALL_STACK_DIR = '../dataset/call_stack'
# 根据源数据和 field 分析出调用链关系
# 调用链分三组：all、outer、inner
class CallStack:
  def __init__(self):
    self.reportLoader = ReportLoader()
    self.fieldLoader = FieldLoader()
    pass

  def save(self, id, call_stacks):
    with open(CALL_STACK_DIR + '/call_data-' + str(id) + '.json', 'w') as outfile:
      json.dump(call_stacks, outfile)
  
  def fetch_call_stacks(self, stack, start, end):
    calls = stack['calls']
    result = []
    for i in range(1, len(calls)):
      if i < start or i > end: continue
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
      stack_arr = stack_arrs[i]
      # call_stack1 = self.fetch_call_stacks(stack_arr, start, end)
      call_stack2 = self.fetch_call_stacks(stack_arr, 0, start)
      call_stack3 = self.fetch_call_stacks(stack_arr, end, len(stack_arr))
      call_stack4 = self.fetch_call_stacks(stack_arr, 0, len(stack_arr))
      call_stack5 = self.fetch_call_stacks(stack_arr, start - 1 if start > 0 else 0, end + 1)
      calls = {
        'inner': call_stack5,
        'outer_pre': call_stack2,
        'outer_suf': call_stack3,
        'all': call_stack4
      }
      result.append(calls)
    self.save(id, result)
    # print('Done!')

def main():
  print('Start...')
  callStack = CallStack()
  # callStack.start(450177)

  reportLoader = ReportLoader()
  ids = reportLoader.load_id_from_dir()
  print('Total ids: ', len(ids))
  for id in ids:
    # print('current: ', id)
    callStack.start(id)
  print('Done!')
  # print(FieldLoader().load_field(450177))

main()