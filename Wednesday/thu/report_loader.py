import json, os

# JSON_DIR = '../dataset/json_copy'
JSON_DIR = '../dataset/json'

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