import json
import os
from itertools import combinations
from sklearn.metrics import classification_report

JSON_DIR = '/home/vergil/Projects/stack/stacks.json'
BUCKET_DIR = '/home/vergil/Projects/stack/buckets_.json'

class BucketUtils:
    def __init__(self):
        self.data = json.load(open(BUCKET_DIR))
        # self.result = json.load(open('temp_buckets.json'))
        self.result = self.format()
        try:
            with open('temp_buckets.json', 'w') as outfile:
                json.dump(self.result, outfile)
        except:
            pass

    def fetch_stack_ids(self, bucket_id):
        stack_ids = []
        for dict_ in self.data:
            stack_id_ = dict_['stack_id']
            bucket_id_ = dict_['bucket_id']
            if bucket_id == bucket_id_:
                stack_ids.append(stack_id_)
        return stack_ids
    
    def flattern(self, src_list_):
        return list(set(src_list_))

    def fetch_bucket_ids(self):
        bucket_ids = []
        for dict_ in self.data:
            bucket_id = dict_['bucket_id']
            bucket_ids.append(bucket_id)
        return self.flattern(bucket_ids)

    def format(self):
        bucket_ids = self.fetch_bucket_ids()
        result = {}
        for bucket_id in bucket_ids:
            # print('current bucket id: ', bucket_id)
            stack_ids = self.fetch_stack_ids(bucket_id)
            comb = combinations(stack_ids, 2)
            for ids in comb:
                key1 = str(ids[0]) + ' ' + str(ids[1])
                key2 = str(ids[1]) + ' ' + str(ids[0])
                result.update({
                    key1: True,
                    key2: True
                })
        return result

    def is_right(self, stack_id1, stack_id2):
        key = str(stack_id1) + ' ' + str(stack_id2)
        return self.result.get(key) != None

# 加载文件/处理文件相关格式
class FileUtils:
    def __init__(self):
        def convert(src_stack_arr):
            result = []
            for stack_str in src_stack_arr:
                strs = stack_str.split('.')
                if len(strs) < 2:
                    continue
                # print(strs)
                method = strs[-1]
                classname = strs[-2]
                package = stack_str.replace('.' + classname + '.' + method, '')
                result.append({
                    'package': package,
                    'classname': classname,
                    'method': method
                })
            return result

        def process(stack_json):
            stack_ = json.loads(stack_json)
            calls_ = stack_['raw_stack']
            return convert(calls_)

        json_data = json.load(open(JSON_DIR))
        result = []
        for stack in json_data:
            result.append({
                'stack_id':  stack['id'],
                'stack_arr': process(stack['stack_json'])
            })
        self.data = result

    def load_report(self, id):
        for stack in self.data:
            if stack['stack_id'] == id:
                return stack
        return None

    def load_ids(self):
        ids = []
        for stack in self.data:
            ids.append(stack['stack_id'])
        return ids

# 计算某一 stack 与另一 stack 的结果
class Algorithm:
    def __init__(self):
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

    def fetch_info(self, stack):
        # 获取 sdk 者对外提供的接口函数，以及调用者的函数
        # print(stack)
        apiprovider_package_name = stack[0]['package']
        apiprovider_class_name = stack[0]['classname']
        apiprovider_method_name = stack[0]['method']
        caller_package_name = stack[0]['package']
        caller_class_name = stack[0]['classname']
        caller_method_name = stack[0]['method']
        for i in range(1, len(stack)):
            current_package_name = stack[i]['package']
            if self.jump(current_package_name):
                continue
            if current_package_name == apiprovider_package_name:
                apiprovider_class_name = stack[i]['classname']
                apiprovider_method_name = stack[i]['method']
            else:
                caller_package_name = stack[i]['package']
                caller_class_name = stack[i]['classname']
                caller_method_name = stack[i]['method']
                break
        return {
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

    # private
    def calculate(self, stack_1, stack_2):
        # if stack_1["exception"] != stack_2['exception']:
        #     return False
        if len(stack_1['stack_arr']) == 0 or len(stack_2['stack_arr']) == 0:
            return False
        stack_info1 = self.fetch_info(stack_1['stack_arr'])
        stack_info2 = self.fetch_info(stack_2['stack_arr'])
        return stack_info1 == stack_info2

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
    fileUtils = FileUtils()
    algorithm = Algorithm()
    resultUtils = ResultUtils()
    bucketUtils = BucketUtils()


    # 两两计算，给出 my_id 和另一个 id，返回 True|False
    def cal_result(report1, report2):
        key = str(report1["stack_id"]) + " " + str(report2["stack_id"])
        pred_result = algorithm.calculate(report1, report2)
        real_result = bucketUtils.is_right(report1["stack_id"], report2["stack_id"])
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
        ids = fileUtils.load_ids()
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
        ids = fileUtils.load_ids()
        result = cal_report_to_others(demo_id, ids)
        if showdiff:
            resultUtils.show_diff(result, fliter=fliter) # 会打印运算过程中与真实结果不一致的 id，便于手动检验，非 debug 时可删去该过程
        formated_result = resultUtils.format(result, fliter=fliter)
        return formated_result

    # 启动代码：
    print('配置：')
    start = 0
    end = 10
    fliter = False
    showdiff = True
    print('开始角标：', start)
    print('结束角标：', end)
    print('需要计算的 stack 数据量：', end - start)
    print('是否过滤可能人工未标注的结果：', fliter)
    print('是否打印预测不一致结果：', showdiff) # 即：预测结果与原始结果不一致的情况

    result = run_all(count=(end - start), shift=start, fliter=fliter, showdiff=showdiff)
    print('F1-Score 结果：')
    print(classification_report(result['real_list'], result['pred_list']))
    # print('run: stack_id:: 450132')
    # result = run_demo(450132)
    # print(classification_report(result['real_list'], result['pred_list']))

main()

def test():
    # fileUtils = FileUtils()
    # algorithm = Algorithm()
    # report1 = fileUtils.load_report(2625)
    # report2 = fileUtils.load_report(2618)
    # pred_result = algorithm.calculate(report1, report2)
    # print(pred_result)

    bucketUtils = BucketUtils()
    print(bucketUtils.is_right(2626, 2618))

# test()