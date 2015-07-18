# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from pyh import *
from fetch.mongodb import dataBase
from fetch.teamdata import dict2ASerial
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

myInput = raw_input('please input serial no: ')
while True:
    dictData=dataBase.find(myInput)
    if  dictData is not None:
        break
    else:
        myInput = raw_input('Not found in database,please input serial no again: ')

aSerial = dict2ASerial(dictData)

def calcPercent(ratios):
    percentRatio=[]
    for ratio in ratios:
        if len(ratio)==0:
            percentRatio.append([1,1,1,1])
            continue
        a= 1/(1/float(ratio[0]) + 1/float(ratio[1])+1/float(ratio[2]))
        b = a/float(ratio[0])
        c = a/float(ratio[1])
        d = a/float(ratio[2])
        percentRatio.append([b,c,d,a])
    return percentRatio

page = PyH('My wonderful PyH page')
page.addCSS('myFirstStyleSheet.css')
page.addJS('jquery-1.11.2.js', 'myFirstJS.js')
page << meta(charset='utf-8')
page <<h2('report details')

myTab =page << table(cl='mytab')
thTr=myTab << tr()
thTr << th('场次',id='th_1')  +  th('赛事',id='th_2')  +  th('对阵',id='th_3')  +  th('心水推荐',id='th_4')
thTr << th('威廉',id='th_5')  +  th('立博',id='th_6')  +    th('英特',id='th_7')  +  th('Bet365',id='th_8')
thTr << th('SNAI',id='th_9')  +  th('爆冷',id='th_10')  +    th('预测',id='th_11')  +  th('赛果',id='th_12')


def buildRank(rank):
    if rank:
        return '[' + rank + ']'
    else:
        return rank

def createRatioTable(ratios,tabClass):
    tmpRatio = ratios[0].original
    filterRatios=[ratios[0].original]
    for index,ratio in enumerate(ratios):
        if ','.join(ratio.realTime) == ','.join(tmpRatio):
            continue
        tmpRatio = ratio.realTime
        filterRatios.append(ratio.realTime)

    percentRatios=calcPercent(filterRatios)
    tmptitl=[]
    for titleratio in percentRatios:
       tmptitl.append( '  '.join(map(lambda x:format(x,'.2%'),titleratio)))

    ratioTable=myTr << td(title='\n'.join(tmptitl)) << table(cl=tabClass)

    for filterRtio in filterRatios:
        wlTr = ratioTable << tr()
        if filterRtio:
            wlTr << td(filterRtio[0]) + td(filterRtio[1])+ td(filterRtio[2])
        else:
            wlTr<<td('')+td('')+td('')
    coldStr=''
    deltcnt=0
    changecnt=0
    subFlag=0
    addFlag=0
    for index, ratio in enumerate(filterRatios):
        if index == 0:
            tmpRatio=ratio
            continue
        else:
            if abs(float(ratio[0])-float(tmpRatio[0])) >= 0.5:
                deltcnt=deltcnt+1
            if float(ratio[0]) > float(tmpRatio[0]):
                addFlag=1
            elif float(ratio[0]) < float(tmpRatio[0]):
                subFlag=1
            tmpRatio=ratio
    if (addFlag+subFlag) >=2:
        changecnt=changecnt+1

    subFlag=0
    addFlag=0
    for index, ratio in enumerate(filterRatios):
        if index == 0:
            tmpRatio=ratio
            continue
        else:
            if abs(float(ratio[1])-float(tmpRatio[1])) >= 0.5:
                deltcnt=deltcnt+1
            if float(ratio[1]) > float(tmpRatio[1]):
                addFlag=1
            elif float(ratio[1]) < float(tmpRatio[1]):
                subFlag=1
            tmpRatio=ratio
    if (addFlag+subFlag) >=2:
        changecnt=changecnt+1

    subFlag=0
    addFlag=0
    for index, ratio in enumerate(filterRatios):
        if index == 0:
            tmpRatio=ratio
            continue
        else:
            if abs(float(ratio[2])-float(tmpRatio[2])) >= 0.5:
                deltcnt=deltcnt+1
            if float(ratio[2]) > float(tmpRatio[2]):
                addFlag=1
            elif float(ratio[2]) < float(tmpRatio[2]):
                subFlag=1
            tmpRatio=ratio
    if (addFlag+subFlag) >=2:
        changecnt=changecnt+1

    return deltcnt,changecnt,percentRatios

for i in range(14):
    if i%2:
        myTr= myTab << tr(cl='alt')
    else:
        myTr= myTab << tr()

    myTr << td(aSerial.teamPairs[i].no) + td(aSerial.teamPairs[i].teamType)
    myTr << td(buildRank(aSerial.teamPairs[i].homeTeamRank ) + aSerial.teamPairs[i].homeTeam + ' VS '+buildRank(aSerial.teamPairs[i].visitTeamRank ) +aSerial.teamPairs[i].visitTeam)
    myTr << td(aSerial.teamPairs[i].xinShui.result,title=aSerial.teamPairs[i].xinShui.homeDetail)

    wlRslt = createRatioTable(aSerial.teamPairs[i].willianRatio,'willianTable')
    lbRslt=createRatioTable(aSerial.teamPairs[i].ladbrokesRatio,'ladbrokesTable')
    interRslt=createRatioTable(aSerial.teamPairs[i].interRatio,'interTable')
    betRslt=createRatioTable(aSerial.teamPairs[i].bet365Ratio,'bet365Table')
    snaiRslt=createRatioTable(aSerial.teamPairs[i].snaiRatio,'snaiTable')
    coldStr=''
    if (wlRslt[0]+lbRslt[0]+interRslt[0]+betRslt[0]+snaiRslt[0])>0:
        coldStr='delt 0.5:'+str(wlRslt[0]+lbRslt[0]+interRslt[0]+betRslt[0]+snaiRslt[0])
    if (wlRslt[1]+lbRslt[1]+interRslt[1]+betRslt[1]+snaiRslt[1])>0:
        coldStr='\n'+coldStr+'two sides:'+str(wlRslt[1]+lbRslt[1]+interRslt[1]+betRslt[1]+snaiRslt[1])
    myTr << td(coldStr,cl='cold')

    resultPercent=wlRslt[2][-1][:3]
    maxPctRatio = max(resultPercent)
    analyzeRslt=''
    if resultPercent.index(maxPctRatio) == 0 and aSerial.teamPairs[i].xinShui.result == 3:
        analyzeRslt='3'
    elif resultPercent.index(maxPctRatio) == 1 and aSerial.teamPairs[i].xinShui.result == 1:
        analyzeRslt='1'
    elif resultPercent.index(maxPctRatio) == 2 and aSerial.teamPairs[i].xinShui.result == 0:
        analyzeRslt='0'

    myTr << td(analyzeRslt,cl='analyze')
    myTr << td(aSerial.teamPairs[i].vsResult,cl='result')

page.printOut('result.html')



