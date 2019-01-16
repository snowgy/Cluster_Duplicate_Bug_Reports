from callstack import CallStackLoader
from field import FieldLoader

class Start:
  def __init__(self):
    self.callStackLoader = CallStackLoader()
    self.fieldLoader = FieldLoader()

  def pipe(self, stack_id1, stack_id2):
    call_stacks1 = self.callStackLoader.load_call_stack(stack_id1)
    fields1 = self.fieldLoader.load_field(stack_id1)
    call_stacks2 = self.callStackLoader.load_call_stack(stack_id2)
    fields2 = self.fieldLoader.load_field(stack_id2)
    
    pass
