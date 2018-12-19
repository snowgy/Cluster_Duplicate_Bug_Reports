import re
import json

class StackTraceExtractor:
  def __init__(self):
    # self.JAVA_TRACE = r'\s*?at\s+([\w<>\$_]+\.)+([\w<>\$_]+)\s*\((.+?)\.java:?(\d+)?\)'
    # 支持负行数：
    self.JAVA_TRACE = r'\s*?at\s+([\w<>\$_]+\.)+([\w<>\$_]+)\s*\((.+?)\.java:?(-\d+|\d+)?\)'
#   at org.eclipse.net4j.util.container.IPluginContainer.<clinit>(IPluginContainer.java:25)

    # These two are for more 'strict' stack trace finding
    # self.JAVA_EXCEPTION = r'\n(([\w<>\$_]++\.?)++[\w<>\$_]*+(Exception|Error){1}(\s|:))'
    # self.JAVA_CAUSE = r'(Caused by:).*?(\w*Exception|\w*Error):(.*?)(\s+at.*?\(.*?:\d+\))+'
    # self.JAVA_CAUSE = r'(Caused by:\s|\s)(([\w<>\$_]+\.)+[\w<>\$_]*(?:Exception|Error)):(.*?)'
    # self.JAVA_CAUSE = r'(Caused by:\s|\s)(([\w<>\$_]+\.)*\w*(?:Exception|Error)):(.*?)'
    self.JAVA_CAUSE = r'(Caused by:\s|\s)(([\w<>\$_]+\.)*\w*(?:Exception|Error)):(.*?)'
    self.RE_FLAGS = re.I | re.M | re.S

    self.TRACE = r'\s*?at\s+(([\w<>\$_]+\.)+([\w<>\$_]+))\s*\((.+?)\.java:?(-\d+|\d+)?\)'
    # self.TRACE = r'\s*?at\s+(([\w<>\$_]+\.)*)([\w<>\$_]+)\((.+?)\.java:?(-\d+|\d+)?\)\s'
    # self.TRACE = r'\s*?at\s+(([\w<>\$_]+\.)*)([\w<>\$_]+)\((.+?)\.java:?(-\d+|\d+)?\)\s'
    # (packagename, classname, methodname, filename, fileline)

  def find_stack_traces(self, s):
    lines = s.split("\n")
    stack_traces = []
    current_calls = []
    index = 0
    while index < len(lines):
      # print(lines[i])
      causebys = re.findall(re.compile(self.JAVA_CAUSE, self.RE_FLAGS), lines[index])
      if len(causebys) != 0:
        # 底下的就是堆栈信息
        causeby = causebys[0]
        # print('\n\n\n\n\n\n\n\n')
        # print(causeby)
        current_calls = []
        stack_traces.append({
          'exception': causeby[1],
          'calls': current_calls
        })
      calls = re.findall(re.compile(self.TRACE, self.RE_FLAGS), lines[index])
      if len(calls) != 0:
        call = calls[0]
        # print(call)
        package = call[0].replace('.' + call[1] + call[2], '')
        current_calls.append({
          'package': package,
          'class': call[1][:-1],
          'method': call[2],
          'filename': call[3],
          'line': call[4],
        })
      index += 1
    return stack_traces

    # for r in re.findall(re.compile(self.JAVA_CAUSE + self.TRACE, self.RE_FLAGS), s):
    #   # if "Native Method" not in r[2]:
    #   print(r)
        # item = (r[0] + r[1], r[2] + ":" + r[3])
        # print(item)
        # if item not in stack_traces:
        # stack_traces.append(item)

    # for r in re.findall(re.compile(self.JAVA_TRACE, self.RE_FLAGS), s):
    #   if "Native Method" not in r[2]:
    #     item = (r[0] + r[1], r[2] + ":" + r[3])
    #     # if item not in stack_traces:
    #     stack_traces.append(item)

    return stack_traces