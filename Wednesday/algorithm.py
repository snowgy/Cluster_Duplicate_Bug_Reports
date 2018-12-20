import json
import os
from itertools import combinations
from sklearn.metrics import classification_report

JSON_DIR = '../dataset/json'

# 加载文件/处理文件相关格式
class FileUtils:
    def load_report(self, id):
        reportfile = open(JSON_DIR + '/stack_data-' + str(id) + '.json')
        return json.load(reportfile)

    def fetch_id(self, report_file_name):
        return int(report_file_name[11:-5])

    def load_id_from_dir(self, path):
        ids = []
        filenames = os.listdir(path)
        for filename in filenames:  # 遍历文件夹
            report_id = self.fetch_id(filename)
            ids.append(report_id)
        return ids

# 计算某一 stack 与另一 stack 的结果
class Algorithm:
    # private
    def calculate(self, stack_1, stack_2):
        global i_2, i_1
        if stack_1["exception"] != stack_2['exception']:
            return False

        package_name = stack_1["calls"][0]["package"]
        for i_1 in range(len(stack_1["calls"])):
            if stack_1["calls"][i_1]["package"] != package_name:
                break

        for i_2 in range(len(stack_2["calls"])):
            if stack_2["calls"][i_2]["package"] != package_name:
                break

        # if stack_1["calls"][i_1 - 1] == stack_2["calls"][i_2 - 1] and stack_1["calls"][i_1 - 2] == stack_2["calls"][i_2 - 2]:
        #     if stack_1["calls"][i_1] == stack_2["calls"][i_2] and stack_1["calls"][i_1+1] == stack_2["calls"][i_2+1]:
        #         if stack_1["calls"][0] == stack_2["calls"][0]:
        #             return True

        if stack_1["calls"][i_1 - 1] == stack_2["calls"][i_2 - 1]:
            if stack_1["calls"][i_1] == stack_2["calls"][i_2]:
                return True
        # default
        return False

    def start(self, report_set1, report_set2):
        try:
            for stack_0 in report_set1["stack_arr"]:
                for stack_1 in report_set2["stack_arr"]:
                    if self.calculate(stack_0, stack_1):
                        return True
            return False
        except:
            # print(report_set1["stack_id"])
            return False

# 结果处理
class ResultUtils:
    # 弃用
    # 辅助，将 dict 转换为 list (去掉 key)
    def to_list(self, dict_):
        list_ = []
        for v in dict_.values():
            list_.append('TRUE' if v else 'FALSE')
        return list_

    # [{'450439 275972': [False, False]}] => [False] [False]
    # [{'450439 275972': [False, False]}, {'450439 16749': [False, False]}] => [False, False] [False, False]
    def format(self, src_list):
        list1 = [] # real
        list2 = [] # pred
        for dict_ in src_list:
            for v in dict_.values():
                list1.append(v[0])
                list2.append(v[1])
        return {'real_list': list1, 'pred_list': list2}

    # 把多组运算结果合并
    # [{'real_list': [False, False], 'pred_list': [False, False]}] => {'real_list': [False, False], 'pred_list': [False, False]}
    def combine(self, src_list):
        list1 = []
        list2 = []
        for dict_ in src_list:
            real_list = dict_['real_list']
            pred_list = dict_['pred_list']
            list1 += real_list
            list2 += pred_list
        return {'real_list': list1, 'pred_list': list2}

    # （辅助函数）打印两个数组不同处
    def show_diff(self, list1, list2):
        if len(list1) != len(list2):
            return
        index = 0
        for i in range(0, len(list1)):
            if list1[i] == 'TRUE' or list2[i] == 'TRUE':
                print(index, list1[i], list2[i])
                pass
            i += 1




def main():
    fileUtils = FileUtils()
    algorithm = Algorithm()
    resultUtils = ResultUtils()

    # 两两计算，给出 my_id 和另一个 id，返回 True|False
    def cal_result(report1, report2):
        key = str(report1["stack_id"]) + " " + str(report2["stack_id"])
        pred_result = algorithm.start(report1, report2)
        real_result = str(report2["stack_id"]) in report1["duplicated_stack_id"]
        return {key: [real_result, pred_result]}

    # 两两计算，给出 my_id 和 其余所有的 id，返回 [True|False]
    def cal_report_to_others(my_id, ids):
        # ids = load_id_from_dir(JSON_DIR)
        result = []
        reportme = fileUtils.load_report(my_id)
        for report_id in ids:
            if report_id == my_id: # 不与自己计算
                continue
            report = fileUtils.load_report(report_id)  # 加载为 json
            result.append(cal_result(reportme, report))
        return result
    
    # 正式运算，耗时
    def run_all():
        results = []
        ids = fileUtils.load_id_from_dir(JSON_DIR)
        result = cal_report_to_others(450439, ids)
        formated_result = resultUtils.format(result)
        for report_id in ids:  # 遍历文件夹
            result = cal_report_to_others(report_id, ids)
            formated_result = resultUtils.format(result)
            results.append(formated_result)
        return resultUtils.combine(results)

    # 示例运算，计算其中的一个 id 与 其余所有 的结果
    def run_demo(demo_id):
        ids = fileUtils.load_id_from_dir(JSON_DIR)
        result = cal_report_to_others(demo_id, ids)
        formated_result = resultUtils.format(result)
        return formated_result

    # 启动代码：
    # result = run_all()
    # print(classification_report(result['real_list'], result['pred_list']))
    result = run_demo(450439)
    print(classification_report(result['real_list'], result['pred_list']))

main()
