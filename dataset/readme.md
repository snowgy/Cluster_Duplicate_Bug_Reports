## 原始数据 headers:

* Issue_id
* Priority
* Component
* Duplicated_issue
* Title
* Description
* Status
* Resolution
* Version
* Created_time
* Resolved_time

## JSON 数据:

##### 格式如下
```javascript
[
  {
    "stack_id": 0,
    "reported_time": "2014-11-07 04:22",
    "modified_time": "2015-09-15 15:01",
    "stack_arr": [
      {
        "symbol": "main",
        "file": "main.java",
        "line": 100
      },
      {
        "symbol": "Sort.quick_sort",
        "file": "Sort.java",
        "line": 123
      },
      {
        "symbol": "Sort.print_result",
        "file": "Sort.java"
        "line": 111
      }
    ],
    "duplicated_stack_id": -1
  }
]
```

## 依赖：

```
pip3 install requests
pip3 install beautifulsoup4
```