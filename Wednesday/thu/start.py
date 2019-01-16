from callstack import CallStackLoader
from field import FieldLoader

# 比较两个 stack report 内的第 0 个 stack 信息
# 二次信息（非原始数据，stack.json -> call_data.json + field_data.json）
class Start:
  def __init__(self):
    self.callStackLoader = CallStackLoader()
    self.fieldLoader = FieldLoader()

  # 计算开始
  def calculate(self, report_id1, report_id2):
    call_stacks1 = self.callStackLoader.load_call_stack(report_id1)
    fields1 = self.fieldLoader.load_field(report_id1)
    call_stacks2 = self.callStackLoader.load_call_stack(report_id2)
    fields2 = self.fieldLoader.load_field(report_id2)

    # 暂时只对比两个 report 中各自第一个 stack 数据
    field1 = fields1[0]
    field2 = fields2[0]
    callstack1 = call_stacks1[0]
    callstack2 = call_stacks2[0]
    ## calls
    # 'exception'
    # 'inner'
    # 'outer_pre'
    # 'outer_suf'
    # 'all'
    
    ## field
    # 'field': field_area, # [[]...]
    # 'deep': field_deep, # 3
    # 'interest_field': interest['package'], # org.eclipse.swt
    # 'interest_length': interest['length'], # 38
    # 'interest_start': interest['start_index'], # 0
    # 'interest_end': interest['end_index'] # 37

    return {
      'exception': 1 if callstack1['exception'] == callstack2['exception'] else 0, # exception 是否相同
      # 'exception_msg': 1, # exception message 是否相同
      'field_isdup': 1, # field 是否为包含关系
      'field_dup_index': 0.82, # field 重合指数，即覆盖率
      'field_deep': 1, # field 深度 比例，比如：4/5
      'field_length': 1, # field 长度 比例，比如：4/5
      'field_interest_issame': 1, # 核心 field 区域是否一致，比如：org.eclipse.swt == org.eclipse.swt
      'field_interest_length': 1, # 核心 field 区域长度 比例，比如：4/5
      'callstack_inner': 0.83, # 核心 callstack 区域调用链相似度
      'callstack_outer_1': 0.8, # 除开核心 callstack 区域，顶部区域相似度
      'callstack_outer_2': 0.4, # 除开核心 callstack 区域，底部区域相似度
      'callstack_all': 0.7, # 全部区域相似度
      'is_dup': 1 # 是否为相同 bug，靠上面所有的数据得出该结论
    }
    # return {
    #   'exception': 1, # exception 是否相同
    #   # 'exception_msg': 1, # exception message 是否相同
    #   'field_isdup': 1, # field 是否为包含关系
    #   'field_dup_index': 0.82, # field 重合指数，即覆盖率
    #   'field_deep': 1, # field 深度 比例，比如：4/5
    #   'field_length': 1, # field 长度 比例，比如：4/5
    #   'field_interest_issame': 1, # 核心 field 区域是否一致，比如：org.eclipse.swt == org.eclipse.swt
    #   'field_interest_length': 1, # 核心 field 区域长度 比例，比如：4/5
    #   'callstack_inner': 0.83, # 核心 callstack 区域调用链相似度
    #   'callstack_outer_1': 0.8, # 除开核心 callstack 区域，顶部区域相似度
    #   'callstack_outer_2': 0.4, # 除开核心 callstack 区域，底部区域相似度
    #   'callstack_all': 0.7, # 全部区域相似度
    #   'is_dup': 1 # 是否为相同 bug，靠上面所有的数据得出该结论
    # }
