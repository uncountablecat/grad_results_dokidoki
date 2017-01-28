# grad_results_dokidoki
有了这个，你就可以过上不用打开网页也能查询admission result的dokidoki的生活
### 说明
本脚本从 http://thegradcafe.com/survey/index.php 抓取 grad cafe 论坛上的录取数据。

### 使用
在终端中输入`python main.py`，然后按照提示输入你所感兴趣的专业。例：
```python
Your-MacBook-Air:~ excited$ python main.py
Enter Majors, separated by comma:Mathematics,Statistics
``` 

### 输出

一个无辜的csv

### 待解决的问题
1. 有时候会有莫名其妙的引号。例如
```
"""University Of Washington Seattle","(Applied Mathematics), PhD (F17)",Rejected via E-mail on 26 Jan 2017 ,I,26 Jan 2017
```
2. 增加按照提交日期filter的功能
3. 统一所有学校的名字。例如，`UCLA`和`University of California, Los Angeles`都将被写入为`UCLA`

### 啥时候完成？

不知道，等春节结束吧。
