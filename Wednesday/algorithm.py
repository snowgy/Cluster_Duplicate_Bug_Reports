import json
import os
from itertools import combinations
from sklearn.metrics import classification_report
from stack_package_index import StackPackageIndex
from thu.report_loader import ReportLoader

# 计算某一 stack 与另一 stack 的结果
class Algorithm:
    def __init__(self):
        self.stackPackageIndex = StackPackageIndex()
        self.fliter_package = [
            "dalvik.system",
            "java.lang",
            "android",
        ]

    def jump(self, package_name):
        for fliter_name in self.fliter_package:
            if package_name.startswith(fliter_name):
                return True
        return False
    
    def equals(self, stack_info1, stack_info2):
        def not_null(c):
            return c['package'] != None and c['classname'] != None and c['methodname'] != None
        def equal_detail(c1, c2):
            if not_null(c1) and not_null(c2):
                return c1['package'] == c2['package'] \
                    and c1['classname'] == c2['classname'] \
                    and c1['methodname'] == c2['methodname']
            return False

        if stack_info1 == stack_info2:
            if stack_info1['exception'] == stack_info2['exception']:
                return equal_detail(stack_info1['apiprovider'], stack_info2['apiprovider']) \
                    and equal_detail(stack_info1['caller'], stack_info2['caller'])
        return False

    def fetch_info(self, stack):
        # 获取 sdk 者对外提供的接口函数，以及调用者的函数
        # print(stack)
        exception_name = stack['exception']

        calls = stack['calls']
        caller_package_name = None
        caller_class_name = None
        caller_method_name = None
        apiprovider_package_name = None
        apiprovider_class_name = None
        apiprovider_method_name = None
        # filename, line 暂未用到

        for i in range(0, len(calls)):
            current_package_name = calls[i]['package']
            if self.jump(current_package_name):
                continue
            # print('>> index:', i)
            if caller_package_name == None:
                caller_package_name = current_package_name

            if current_package_name == caller_package_name: # 直到找到 caller 最后一行，该行为 调用方法触发行
                # print('>> current package name: ', current_package_name)
                caller_class_name = calls[i]['class']
                caller_method_name = calls[i]['method']
                continue
            else:
                apiprovider_package_name = calls[i]['package']
                apiprovider_class_name = calls[i]['class']
                apiprovider_method_name = calls[i]['method']
                # print('>> current package name: ', current_package_name)
                break

        return {
            'exception': exception_name,
            'apiprovider': {
                'package': apiprovider_package_name,
                'classname': apiprovider_class_name,
                'methodname': apiprovider_method_name
            },
            'caller': {
                'package': caller_package_name,
                'classname': caller_class_name,
                'methodname': caller_method_name
            }
        }
    def calculate(self, stack_id1, stack_id2, stack_1, stack_2):
        if stack_1["exception"] != stack_2['exception']:
            return False
        # print(stack_2['exception'])
        # print(len(stack_1['calls']))
        # step1 计算 stack 是否为同领域，包含关系 或者 重合指数大于 80%
        package_index = self.stackPackageIndex.calculate(stack_id1, stack_id2)
        if not package_index['is_contain'] \
          and package_index['dup_index'] < 0.8:
          return False

        if len(stack_1['calls']) == 0: return False
        if len(stack_2['calls']) == 0: return False
        stack_info1 = self.fetch_info(stack_1)
        stack_info2 = self.fetch_info(stack_2)
        return self.equals(stack_info1, stack_info2)

    def start(self, report_set1, report_set2):
        try:
            if len(report_set1["stack_arr"]) == 0 \
                or len(report_set1["stack_arr"]) == 0:
                # print('len == 0')
                return False
            # #demo
            # if self.calculate(report_set1["stack_arr"][0], report_set2["stack_arr"][0]):
            #     return True
            for stack_0 in report_set1["stack_arr"]:
                for stack_1 in report_set2["stack_arr"]:
                    if self.calculate(report_set1["stack_id"], report_set2["stack_id"], stack_0, stack_1):
                        return True
            return False
        except Exception as e:
            print(report_set1["stack_id"], report_set2["stack_id"])
            print(str(e))
            return False

# 结果处理
class ResultUtils:
    # 弃用，不需要再把 Bool 转化为 String 了
    # 辅助，将 dict 转换为 list (去掉 key)
    def to_list(self, dict_):
        list_ = []
        for v in dict_.values():
            list_.append('TRUE' if v else 'FALSE')
        return list_

    # fliter: 表示是否去除 real: False, pred: True 的数据，这类数据很有可能是预测成功但未人工标记的数据
    # [{'450439 275972': [False, False]}] => [False] [False]
    # [{'450439 275972': [False, False]}, {'450439 16749': [False, False]}] => [False, False] [False, False]
    def format(self, src_list, fliter=False):
        # print('Fliter: ', fliter)
        list1 = [] # real
        list2 = [] # pred
        for dict_ in src_list:
            for v in dict_.values():
                if fliter == True:
                    if v[0] == False and v[1] == True:
                        continue
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
    # fliter: 表示是否去除 real: False, pred: True 的数据，这类数据很有可能是预测成功但未人工标记的数据
    # [{'450439 275972': [False, False]}]
    def show_diff(self, dicts, fliter=False):
        for dict_ in dicts:
            for k, v in dict_.items():
                if fliter == True:
                    if v[0] == False and v[1] == True:
                        continue
                if v[0] != v[1]:
                    print('\t', k, v[0], v[1])

    # 弃用
    # （辅助函数）打印两个数组不同处
    # [False, False], [False, True]
    def show_diff_with_formated_result(self, list1, list2):
        if len(list1) != len(list2):
            return
        for i in range(0, len(list1)):
            if list1[i] == True or list2[i] == True:
                print(i, list1[i], list2[i])




def main():
    fileUtils = ReportLoader()
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
    
    # 正式运算，耗时，可设定最大计算个数 count、偏移量 shift
    def run_all(count=100, shift=0, fliter=False, showdiff=False):
        results = []
        index = 0
        ids = fileUtils.load_id_from_dir()
        print('总共将要比对的 report 数量：', len(ids))
        print('==================== 开始计算！====================')
        for report_id in ids:  # 遍历文件夹
            index += 1
            if index <= shift: continue
            if index >= count + shift + 1: # 设定最多处理的条数，否则每次都跑完所有的数据会很耗时
                return resultUtils.combine(results)
            ## start
            print('进度：%.3f%%' %(100 * (index - shift) / count), '\tcurrent stack_id: ' + str(report_id))
            result = cal_report_to_others(report_id, ids)
            if showdiff:
                resultUtils.show_diff(result, fliter=fliter) # 会打印运算过程中与真实结果不一致的 id，便于手动检验，非 debug 时可删去该过程
            formated_result = resultUtils.format(result, fliter=fliter)
            results.append(formated_result)
        return resultUtils.combine(results)

    # 示例运算，计算其中的一个 id 与 其余所有 的结果
    def run_demo(demo_id, fliter=False, showdiff=False):
        ids = fileUtils.load_id_from_dir()
        result = cal_report_to_others(demo_id, ids)
        if showdiff:
            resultUtils.show_diff(result, fliter=fliter) # 会打印运算过程中与真实结果不一致的 id，便于手动检验，非 debug 时可删去该过程
        formated_result = resultUtils.format(result, fliter=fliter)
        return formated_result

    # 启动代码：
    print('配置：')
    start = 10
    end = 20
    fliter = False
    showdiff = True
    print('开始角标：', start)
    print('结束角标：', end)
    print('需要计算的 stack 数据量：', end - start)
    print('是否过滤可能人工未标注的结果：', fliter)
    print('是否打印预测不一致结果：', showdiff) # 即：预测结果与原始结果不一致的情况

    result = run_demo(450178, fliter=fliter, showdiff=showdiff)
    # result = run_all(count=(end - start), shift=start, fliter=fliter, showdiff=showdiff)
    print('F1-Score 结果：')
    print(classification_report(result['real_list'], result['pred_list']))
    # print('run: stack_id:: 450132')
    # result = run_demo(450132)
    # print(classification_report(result['real_list'], result['pred_list']))

main()

def test():
    fileUtils = ReportLoader()
    algorithm = Algorithm()
    report_test1 = fileUtils.load_report(450177)
    report_test2 = fileUtils.load_report(450180)
    print(algorithm.fetch_info(report_test1["stack_arr"][0]))
    print(algorithm.fetch_info(report_test2["stack_arr"][0]))

# test()