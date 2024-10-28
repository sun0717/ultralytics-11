## 提交规范：
feat: 增加模块
fix: 修代码
docs: 更新readme日志
## 搜索规范
搜索 ctrl + f 搜索增加/删除/修改地方：
`#sun add(update、delete) here`  
## 训练规范
日期、模块名称、batch、mAP、存储地址
### 9-30
base11s - 16 - 0.395 - runs/detect/train3 
base11m - 16 - 0.408 - runs/detect/train4
### 10-02
feat: ASFF modules - 16 - 0.405 - runs/detect/train5

feat: CAFM modules - 16 - 0.392 - 16 层出去的 - runs/detect/train6

### 10-03
feat: CAFM modules - 16 - 0.403 - 17 层出去的 - runs/detect/train6
### 10-04
feat: cafm-asff - 16 - 0.394 - runs/detect/train8
### 10-05
feat: evc -16 - 0.396 - runs/detect/train9
### 10-07
feat: rtdetr - 8 - 0.394 - runs/detect/train12
### 10-08
feat: SPDConv - 16- 0.396 - runs/detect/train13   (剪枝可用)
### 10-09
feat: cleanScript & ScConv in backbone - 16 - 0.408 - runs/detect/train13
### 10-14
feat: scconv + asff - 16 - 0.4 -runs/detect/train15
### 10-15
### 10-21
feat: c2f-scconv - 16 - 0.379 -runs/detect/train18
### 10-22
c3k2-scconv - 16 - 0.394 -runs/detect/train19
改成两个 True 0.386 -runs/detect/train20
### 10-23
两个 False 0.5 - 0.392 - 16
两个 False 0.25 - 0.394 - 16
两个 False 1 - 0.389
四个 False 0.25 - 0.387
False True False True 0.25 - 0.39
### 10-27
True False True False 0.25 - 0.384