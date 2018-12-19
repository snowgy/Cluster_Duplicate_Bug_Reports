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
    "stack_id": 450440,
    "component": "Recommenders",
    "importance": "P3 normal",
    "reported_time": "2014-11-07 04:22",
    "modified_time": "2015-09-15 15:01",
    "stack_arr": [
      {
        "exception": "org.osgi.framework.BundleException",
        "calls": [
          {
            "package": "org.eclipse.osgi.internal.framework",
            "class": "BundleContextImpl.",
            "method": "start",
            "filename": "BundleContextImpl",
            "line": "711"
          },
          {
            "package": "org.eclipse.osgi.internal.framework",
            "class": "EquinoxBundle.",
            "method": "startWorker0",
            "filename": "EquinoxBundle",
            "line": "941"
          }
        ]
      },
      {
        "exception": "java.lang.ClassNotFoundException",
        "calls": [
          {
            "package": "org.eclipse.osgi.internal.hooks",
            "class": "EclipseLazyStarter.",
            "method": "postFindLocalClass",
            "filename": "EclipseLazyStarter",
            "line": "116"
          },
          {
            "package": "org.eclipse.osgi.internal.loader.classpath",
            "class": "ClasspathManager.",
            "method": "findLocalClass",
            "filename": "ClasspathManager",
            "line": "531"
          }
        ]
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