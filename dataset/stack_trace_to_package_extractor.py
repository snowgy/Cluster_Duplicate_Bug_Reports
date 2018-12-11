import re


class StackTraceExtractor:
    def __init__(self):
        # self.JAVA_TRACE = r'\s*?at\s+([\w<>\$_]+\.)+([\w<>\$_]+)\s*\((.+?)\.java:?(\d+)?\)'
        # 支持负行数：a
        self.JAVA_TRACE = r'\s*?at\s+((?:[\w<>\$_]+\.)+)(?:[\w<>\$_]+)\s*\((.+?)\.java:?(-\d+|\d+)?\)'

        # These two are for more 'strict' stack trace finding
        self.JAVA_EXCEPTION = r'\n(([\w<>\$_]++\.?)++[\w<>\$_]*+(Exception|Error){1}(\s|:))'
        self.JAVA_CAUSE = r'(Caused by:).*?(Exception|Error)(.*?)(\s+at.*?\(.*?:\d+\))+'
        self.RE_FLAGS = re.M | re.S

    def find_stack_traces(self, s):
        stack_traces = []

        for r in re.findall(re.compile(self.JAVA_TRACE, self.RE_FLAGS), s):
            if "Native Method" not in r[1]:
                item = (r[0][:-1], r[1] + ":" + r[2])
                if item not in stack_traces:
                    stack_traces.append(item)

        return stack_traces

