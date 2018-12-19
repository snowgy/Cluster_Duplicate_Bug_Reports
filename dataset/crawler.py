# 爬取同时会执行数据解析，判断是否含有 stack trace，如果有，则解析保存，否则跳过

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
    if not soup:
      return None
    comments = soup.find(id="c0", class_="bz_first_comment")
    if not comments:
      return None
    _description = comments.find("pre").text
    frames = self.stackTraceExtractor.find_stack_traces(_description)
    # print(frames)
    if len(frames) is 0:
      return None
    edit_form = soup.find("table", class_="edit_form")
    # print(edit_form)
    duplicates_span = edit_form.find("span", id="duplicates")
    _duplicates = []
    if duplicates_span:
      duplicates = duplicates_span.find_all("a")
      for i in range(0, len(duplicates)):
        _duplicates.append(duplicates[i].text)
      # print(_duplicates)
    _static_bug_status = edit_form.find(id="static_bug_status").string
    _field_container_product = edit_form.find(id="field_container_product").string
    _field_container_component = edit_form.find(id="field_container_component").text.replace("(show other bugs)", "").strip()
    _vcard = edit_form.find_all(class_="vcard")[0].find_all("a")[0].get("href")[24:]
    left_edit_form = edit_form.find_all("td", id="bz_show_bug_column_1")[0].find_all("tr")
    _importance = left_edit_form[10].find_all("td")[0].text.replace("(vote)", "").replace("\n", "").replace("       ", " ").strip()

    time_trs = edit_form.find_all("td", id="bz_show_bug_column_2")[0].find_all("tr")
    _reported_time = time_trs[0].find_all("td")[0].text[:16]
    _modified_time = time_trs[1].find_all("td")[0].text[:16]
    # print(_description)
    return {
      "stack_id": stack_id,
      "component": _field_container_component,
      "importance": _importance,
      "reported_time": _reported_time,
      "modified_time": _modified_time,
      # "stack_arr": self.convert_to_json(frames)
      "stack_arr": frames,
      "duplicated_stack_id": _duplicates
    }

# crawler = Crawler()
# result = crawler.fetch_data(450440)
# print(result)


# 示例：爬取 id 在区间 [450439, 450440] 的数据：
# crawler = Crawler()
# result_list = []
# for id in range(450439, 450451):
#   try:
#     result = crawler.fetch_data(id)
#     if result is not None:
#       result_list.append(result)
#   except:
#     pass

# with open('dataset/stack_data.json', 'w') as outfile:
#   json.dump(result_list, outfile)

crawler = Crawler()
for id in range(450439, 450451):
  try:
    result = crawler.fetch_data(id)
    if result is not None:
      with open('dataset/jsons/stack_data-' + str(id) + '.json', 'w') as outfile:
        json.dump(result, outfile)
  except:
    pass


