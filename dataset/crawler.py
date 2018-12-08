## 爬取同时会执行数据解析，判断是否含有 stack trace，如果有，则解析保存，否则跳过

from bs4 import BeautifulSoup
from stack_trace_extractor import StackTraceExtractor
import requests
import json

class Crawler:
  def __init__(self):
    self.stackTraceExtractor = StackTraceExtractor()

  def convert_to_json(self, frames):
    array = []
    for frame in frames:
      # print(frame[1])
      _symbol = frame[0]
      _other = frame[1].split(":")
      _file = _other[0] + ".java"
      _line = int(_other[1])
      array.append({
        "symbol": _symbol,
        "file": _file,
        "line": _line
      })
    return array

  def fetch_data(self, stack_id):
    url = "https://bugs.eclipse.org/bugs/show_bug.cgi?id="
    response = requests.get(url + str(stack_id))
    # print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    _description = soup.find(id="c0", class_="bz_first_comment").find("pre").text
    frames = self.stackTraceExtractor.find_stack_traces(_description)
    # print(frames)
    if len(frames) is 0:
      return None
    edit_form = soup.find("table", class_="edit_form")
    # print(edit_form)
    _static_bug_status = edit_form.find(id="static_bug_status").string
    _field_container_product = edit_form.find(id="field_container_product").string
    _field_container_component = edit_form.find(id="field_container_component").string
    _vcard = edit_form.find_all(class_="vcard")[0].find_all("a")[0].get("href")[24:]
    time_trs = edit_form.find_all("td", id="bz_show_bug_column_2")[0].find_all("tr")
    _reported_time = time_trs[0].find_all("td")[0].text
    _modified_time = time_trs[1].find_all("td")[0].text.replace("(History)", "")
    # print(_description)
    return {
      "stack_id": stack_id,
      "stack_arr": self.convert_to_json(frames)
    }

# crawler = Crawler()
# result = crawler.fetch_data(450440)
# print(result)

# 示例：爬取 id 在区间 [450439, 450440] 的数据：
crawler = Crawler()
result_list = []
for id in range(450439, 450440):
  try:
    result = crawler.fetch_data(450440)
    if result is not None:
      result_list.append(result)
  except:
    pass

with open('stack_data.json', 'w') as outfile:
  json.dump(result_list, outfile)