from start import Starter
from report_loader import ReportLoader
import json


class FliterUtil:
  def __init__(self):
    dupids_file = open('./sim_data/eclipse_data.json')
    self.dup_ids = json.load(dupids_file)
    self.weight = [
      1.8068133,
      0.5780731,
      0.43973943,
      -0.03803377,
      0.21721358,
      1.31300488,
      0.09043153,
      1.19156363,
      0.72639543,
      0.30905945,
      0.42585226
    ]
    self.c = 1.80453293352148
    self.starter = Starter()
    self.reportLoader = ReportLoader()

  def is_empty_stack(self, report_id):
    report = self.reportLoader.load_report(report_id)
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

  def fetch_thu_result(self, report_id1, report_id2):
    dict=self.starter.calculate(report_id1,report_id2)
    print(dict)
    w1 = self.weight[0]
    w2 = self.weight[1]
    w3 = self.weight[2]
    w4 = self.weight[3]
    w5 = self.weight[4]
    w6 = self.weight[5]
    w7 = self.weight[6]
    w8 = self.weight[7]
    w9 = self.weight[8]
    w10 = self.weight[9]
    w11 = self.weight[10]
    sim=dict['exception']*w1+dict['field_isdup']*w2+dict['field_dup_index']*w3+dict[ 'field_deep']*w4+dict['field_length']*w5+dict['field_interest_issame']*w6+dict['field_interest_length']*w7+dict['callstack_inner']*w8+dict['callstack_outer_1']*w9+dict['callstack_outer_2']*w10+dict[ 'callstack_all']*w11
    result = sim > self.c
    if result:
      # 判断是否为 空 堆栈信息
      if self.is_empty_stack(report_id1) or self.is_empty_stack(report_id2):
        return False
      else:
        return True
    return False

  def fetch_eclipse_result(self, report_id1, report_id2):
    result = self.dup_ids[str(report_id1)]
    # print(result)
    if result == []:
      result = self.dup_ids[str(report_id2)]
    if result == []:
      return False
    if str(report_id1) in result: return True
    if str(report_id2) in result: return True
    return False

  def judge_print(self, report_id1, report_id2):
    result1 = self.fetch_thu_result(report_id1, report_id2)
    result2 = self.fetch_eclipse_result(report_id1, report_id2)
    if result1 == result2: return
    if result1 == True and result2 == False: # 我们判断的 T，但 eclipse 给的 F
      print(report_id1, report_id2, "NEED CHECK", "thu: [ T ] eclipse: < F >")
    if result1 == False and result2 == True: # 我们判断的 F，但 eclipse 给的 T
      print(report_id1, report_id2, "NEED CHECK", "thu: < F > eclipse: [ T ]")

  def judge_all(self):
    ids = self.reportLoader.load_id_from_dir()
    for id1 in ids:
      for id2 in ids:
        if id1 == id2: continue
        self.judge_print(id1, id2)

fliter = FliterUtil()
# fliter.judge_all()
fliter.judge_print(463257, 453430)