import json, random

## STEP 2
data = {}

def load_dup_ids():
  dupids = open('./stack_dups_data.json')
  return json.load(dupids)

def fetch_undup_id(data, src_id):
  src_dupids = data.get(str(src_id))
  # random fetch
  index = int((len(data) - 50) * random.random())
  # print(index)
  for id, dupids in data.items():
    if id == src_id: continue
    if src_id in dupids: continue
    if id in src_dupids: continue
    index -= 1
    if index <= 0:
      return int(id)
  return None

def save(rows):
  with open('./stack_test_and_train_data.txt', 'w') as outfile:
    for row in rows:
      line = row + "\n"
      outfile.write(line)
  outfile.close()

def start():
  ## init load data
  data = load_dup_ids()
  result = []
  for id, dupids in data.items():
    if dupids != []:
      undup_id = fetch_undup_id(data, id)
      index = int(len(dupids) * random.random())
      # print(id, dupids[index], undup_id)
      result.append(str(id) + " " + str(dupids[index]) + " " + str(undup_id))
  save(result)
  print("DONE!")

start()