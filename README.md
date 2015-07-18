# football-lottery
用于抓取足彩14场比赛的赔率相关数据并生成报表
## 前提条件
* 安装python2.7.9
* 安装mongodb数据库
* 浏览器能访问连接互联网

## 使用方法
* 抓取足彩胜负14场比赛数据：在项目目录下运行 *python main.py*  该程序会每隔30分钟抓取一次最新数据
* 生成报告：前提是*python main.py*运行至少30分钟以上后，再运行 *python report.py* 在当前目录下生成报告文件report.html
