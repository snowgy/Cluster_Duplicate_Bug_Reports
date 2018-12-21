# 合并所有数据的 dupids
import json
import os

JSON_DIR = 'json_copy'

# 加载文件/处理文件相关格式
class FileUtils:
    def load_report(self, id):
        reportfile = open(JSON_DIR + '/stack_data-' + str(id) + '.json')
        return json.load(reportfile)

    def load_id_from_dir(self, path):
        ids = []
        filenames = os.listdir(path)
        for filename in filenames:  # 遍历文件夹
            report_id = int(filename[11:-5])
            ids.append(report_id)
        return ids
      
class CombineUtils:
    def __init__(self):
        self.fileUtils = FileUtils()

    def fetch_dup_ids(self, id):
        report = self.fileUtils.load_report(id)
        dupids = report['duplicated_stack_id']
        return dupids

    # 把 dupid 加入到 id 的 report 里面
    def update_report(self, to, id):
        try:
            report = self.fileUtils.load_report(to)
            dupids = report['duplicated_stack_id']
            strid = str(id)
            for dupid in dupids:
                if dupid == strid:
                    return
            dupids.append(strid)
            report['duplicated_stack_id'] = list(set(dupids))
            with open(JSON_DIR + '/stack_data-' + str(to) + '.json', 'w') as outfile:
                json.dump(report, outfile)
        except:
            print('No such report, id: ', to)
            pass
        
    def start(self):
        ids = self.fileUtils.load_id_from_dir(JSON_DIR)
        for report_id in ids:
            print('current report id: ', report_id)
            dupids = self.fetch_dup_ids(report_id)
            if len(dupids) == 0:
                continue
            for dupid in dupids:
                self.update_report(to=dupid, id=report_id)
def main():
    combineUtils = CombineUtils()
    combineUtils.start()
    # combineUtils.update_report(to=450439, id=450440)

main()