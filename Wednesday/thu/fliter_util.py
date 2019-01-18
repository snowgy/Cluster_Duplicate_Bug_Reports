from start import Starter


class FliterUtil:
  def __init__(self):
    self.weight = []
    self.c = 0.8
    self.starter = Starter()

  def fetch_thu_result(self, report_id1, report_id2):
    dict=self.starter.calculate(report_id1,report_id2)
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
    return sim > self.c

  def fetch_eclipse_result(self, report_id1, report_id2):
    return True

  def judge_print(self, report_id1, report_id2):
    result1 = self.fetch_thu_result(report_id1, report_id2)
    result2 = self.fetch_eclipse_result(report_id1, report_id2)
    if result1 == result2: return
    if result1 == True and result2 == False: # 我们判断的 T，但 eclipse 给的 F
      print(report_id1, report_id2, "NEED CHECK", "thu: [ T ] eclipse: < F >")
    if result1 == False and result2 == True: # 我们判断的 F，但 eclipse 给的 T
      print(report_id1, report_id2, "NEED CHECK", "thu: < F > eclipse: [ T ]")
