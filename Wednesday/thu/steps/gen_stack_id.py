import json, os, itertools

## STEP 1

JSON_DIR = '../../../dataset/json'

data = {}

def load_report(id):
  # print(id)
  reportfile = open(JSON_DIR + '/stack_data-' + str(id) + '.json')
  return json.load(reportfile)

def load_id_from_dir(path=JSON_DIR):
  ids = []
  filenames = os.listdir(path)
  for filename in filenames:  # 遍历文件夹
    # print(filename)
    if len(filename) < 10: continue
    report_id = int(filename[11:-5])
    ids.append(report_id)
  return ids

def save(data):
  with open('./stack_dups_data.json', 'w') as outfile:
    json.dump(data, outfile)

def load_data():
  data_file = open('./stack_dups_data.json')
  return json.load(data_file)

def update_info(report_id, other_id):    
  key = str(report_id)
  if not key.isdigit(): return
  dt = data.get(key)
  if dt == None: dt = []
  # print(dt)
  if other_id != None:
    value = str(other_id)
    if not value.isdigit(): return
    if value in dt: return
    dt.append(value)
  data.update({key: dt})

# step 1
def start_single_file():
  ids = load_id_from_dir()
  for id in ids:
    report = load_report(id)
    dupids = report['duplicated_stack_id']
    if len(dupids) == 0:
      update_info(id, None)
      continue
    for dupid in dupids:
      update_info(id, dupid)
      update_info(dupid, id)
    dupids.append(id)
    for x in itertools.product(dupids, dupids):
      if str(x[0]).isdigit() and str(x[1]).isdigit():
        key_id = int(x[0])
        val_id = int(x[1])
        if key_id not in ids or val_id not in ids:
          continue
        if key_id != val_id:
          update_info(key_id, val_id)
        
  save(data)
  print("DONE!")

# step 2
def start_save_to_stack():
  ids = load_id_from_dir()
  datas = load_data()
  print("total: ", len(ids))
  for id in ids:
    report = load_report(id)
    report['duplicated_stack_id'] = datas[str(id)]
    with open(JSON_DIR + '/stack_data-' + str(id) + '.json', 'w') as outfile:
      # print(id)
      json.dump(report, outfile)
    
  print("DONE!")

# start_single_file()
start_save_to_stack()