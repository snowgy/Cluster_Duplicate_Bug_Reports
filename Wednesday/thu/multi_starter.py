from start import Starter
from report_loader import ReportLoader
import csv, threading
import multiprocessing as mp

# MIDDLE_RESULT_DIR = '../../dataset/middle_result'
MIDDLE_RESULT_DIR = '../../dataset/middle_result2'

class MultiStarter:
  def __init__(self):
    self.starter = Starter()
    self.reportLoader = ReportLoader()
  
  def fliter_id(self, id):
    return id < 400000 or id > 500000

  def start_all(self, thread_id, start_index, size):
    ids = self.reportLoader.load_id_from_dir()
    index = 0
    end_index = start_index + size
    for id1 in ids:
      if self.fliter_id(id1): continue
      index += 1
      if index < start_index: continue
      if index > end_index: break
      print("%2d"%(thread_id), "current index:", index - start_index)
      # print("%2d"%(thread_id), ">> progress: %.4f" %((index - start_index)/size), "| current_id: ", id1)
      # go:
      with open(MIDDLE_RESULT_DIR + '/starter_result_' + str(id1) + '.csv', 'w') as writeFile:
        for id2 in ids:
          if self.fliter_id(id2): continue
          if id1 == id2: continue
          dict = self.starter.calculate(id1, id2)
          line = [id1, id2, dict['exception'], dict['field_isdup'], dict['field_dup_index'], dict[ 'field_deep'], dict['field_length'], dict['field_interest_issame'], dict['field_interest_length'], dict['callstack_inner'], dict['callstack_outer_1'], dict['callstack_outer_2'], dict[ 'callstack_all']]
          # print(dict)
          writer = csv.writer(writeFile)
          writer.writerow(line)
        writeFile.close()

  def run_all(self):
    for i in range(0, 11):
      size = 400
      start_index = i * size
      print("start index: ", start_index, ", size: ", size)
      t = mp.Process(target=self.start_all, args=(i, start_index, size))
      t.start()

## main:
if __name__ == '__main__':
  MultiStarter().run_all()