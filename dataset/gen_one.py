import json
import os

JSON_DIR = './json'


# 加载文件/处理文件相关格式
class ReportLoader:
    def load_report(self, id):
        reportfile = open(JSON_DIR + '/stack_data-' + str(id) + '.json')
        return json.load(reportfile)

    def load_id_from_dir(self, path=JSON_DIR):
        ids = []
        filenames = os.listdir(path)
        for filename in filenames:  # 遍历文件夹
            report_id = int(filename[11:-5])
            ids.append(report_id)
        return ids


if __name__ == '__main__':
    L = ReportLoader()
    stk_ids = L.load_id_from_dir()
    t_stk_ids = dict()
    t = 0
    for stk_id in stk_ids:
        # t_stk_ids.setdefault(stk_id, L.load_report(stk_id)['duplicated_stack_id'])
        tmp = []
        for i in L.load_report(stk_id)['duplicated_stack_id']:
            try:
                t = int(i)
                if t in stk_ids:
                    tmp.append(i)
                # else:
                #     print(i)
            except:
                pass
        t_stk_ids.setdefault(stk_id, tmp)


    jsObj = json.dumps(t_stk_ids)

    fileObject = open('tmp.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()

    # f = open('tmp.txt', 'w')
    # for stk_id in t_stk_ids:
    #     tmp = str(stk_id) + ','
    #     for dup_id in t_stk_ids[stk_id]:
    #         tmp += dup_id + ','
    #     tmp += '\r'
    #     f.write(tmp)
    #
    # f.close()
