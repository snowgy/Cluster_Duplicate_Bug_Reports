OUT_DIR = "../sim_data"
# MAX_SIZE = 1000

def load_data():
  result = []
  with open('stack_test_and_train_data.txt', 'r') as f:
    result = f.readlines()
  return result

def save(filename, rows):
  with open(OUT_DIR + '/' + filename + '.txt', 'w') as outfile:
    for row in rows:
      outfile.write(row)
  outfile.close()

def start():
  TEST_SIZE = 800
  TRAIN_SIZE = 200
  test = []
  train = []
  data = load_data()
  total_size = len(data)
  ratio = int(total_size / (TEST_SIZE + TRAIN_SIZE)) - 1
  index = 0
  for line in data:
    if index % ratio == 0:
      sp = index % 10
      if sp > 2 and TEST_SIZE > 0:
        test.append(line)
        TEST_SIZE -= 1
      if sp <= 2 and TRAIN_SIZE > 0:
        train.append(line)
        TRAIN_SIZE -= 1
    # print(line)
    index += 1
  # print(len(test))
  # print(len(train))
  save("testing", test)
  save("traning", train)
  print('DONE!')

start()