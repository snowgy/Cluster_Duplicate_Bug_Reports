from sklearn.metrics import classification_report
import os
# y_true = [0, 1, 2, 2, 0]
# y_pred = [0, 1, 2, 2, 3]
y_true = ['a', 1, 2, 2, 3]
y_pred = ['a', 1, 2, 2, 3]
print(classification_report(y_true, y_pred))


filenames = os.listdir('json')
print(len(filenames))