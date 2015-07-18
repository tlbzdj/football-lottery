# -*- coding: utf-8 -*-

import json
import re
import threading
import time
from fetch.mongodb import dataBase

__author__ = 'Administrator'
import requests
from lxml import html

class Refer():
    def __init__(self,result,homeDetail,visitDetail):
        self.result=result
        self.homeDetail=homeDetail
        self.visitDetail=visitDetail
    def build(self,url):
        r = requests.get(url)
        r.encoding='gb2312'
        tree = html.fromstring(r.text)
        extract = [p.replace(u'\xa0', '') for p in tree.xpath('//div[@class="M_content"]/table/tr/td[@class="td_one"]/text()')]
        try:
            winTeam=tree.xpath('//div[@class="M_content"]/table/tr/td[@class="td_one td_center"]/span[@class="mar_right60"]/font/text()')[0].replace(u'\xa0', '')
            if re.search(winTeam,extract[0]) is not None:
                self.result=3
            elif re.search(winTeam,extract[1]) is not None:
                self.result=0
            else:
                self.result=1
            self.homeDetail=tree.xpath('//div[@class="M_content"]/table/tr/td[@class="td_one td_no4"]/text()')[0]
        except IndexError:
            print 'can not get xinshui result\n'


class Ratio():
    def __init__(self):
        self.original=[]
        self.realTime=[]

    def build(self,url,str):
        r = requests.get(url)
        r.encoding='gb2312'
        tree = html.fromstring(r.text)
        para='//table[@id="datatb"]/tr/td[@title="'+ str + '"]/../td/table/tbody/tr/td[@onclick]/text()'
        ratios=tree.xpath(para)

        self.original=ratios[0:3]
        self.realTime=ratios[3:6]
        print "ratio:",self.original,self.realTime,ratios
        return self

class TeamPair():
    def __init__(self,homeTeam,visitTeam):
        self.homeTeam =homeTeam
        self.visitTeam = visitTeam
        self.no=''
        self.teamType=''
        self.ratioUrl=''
        self.xinShuiUrl=''
        self.homeTeamRank=''
        self.visitTeamRank=''
        self.xinShui=Refer('','','')
        self.willianRatio=[]
        self.ladbrokesRatio=[]
        self.interRatio=[]
        self.bet365Ratio=[]
        self.snaiRatio=[]

        self.vsResult=''

class ASerial():
    def __init__(self,serialNo):
        self._id=serialNo
        self.teamPairs=[]


def dict2ASerial(d):
    aSerial = ASerial(d['_id'])
    for t in d['teamPairs']:
        teamPair = TeamPair(t['homeTeam'],t['visitTeam'])
        teamPair.no = t['no']
        teamPair.teamType =t['teamType']
        teamPair.ratioUrl = t['ratioUrl']
        teamPair.xinShuiUrl =t['xinShuiUrl']
        teamPair.visitTeamRank =t['visitTeamRank']
        teamPair.homeTeamRank=t['homeTeamRank']
        teamPair.vsResult=t['vsResult']
        teamPair.xinShui =Refer(t['xinShui']['result'],t['xinShui']['homeDetail'],t['xinShui']['visitDetail'])
        for x in t['willianRatio']:
            ratio=Ratio()
            ratio.original=x['original']
            ratio.realTime=x['realTime']
            teamPair.willianRatio.append(ratio)
        for x in t['ladbrokesRatio']:
            ratio=Ratio()
            ratio.original=x['original']
            ratio.realTime=x['realTime']
            teamPair.ladbrokesRatio.append(ratio)
        for x in t['bet365Ratio']:
            ratio=Ratio()
            ratio.original=x['original']
            ratio.realTime=x['realTime']
            teamPair.bet365Ratio.append(ratio)
        for x in t['snaiRatio']:
            ratio=Ratio()
            ratio.original=x['original']
            ratio.realTime=x['realTime']
            teamPair.snaiRatio.append(ratio)
        for x in t['interRatio']:
            ratio=Ratio()
            ratio.original=x['original']
            ratio.realTime=x['realTime']
            teamPair.interRatio.append(ratio)

        aSerial.teamPairs.append(teamPair)
    return aSerial

class ScrapyModel(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.quitFlag = True
        # self.threadID= threadID
        # self.name = name
    def wait(self,min=30):
        seconds=min*60
        step =5
        for i in range(seconds/step):
            if self.quitFlag:
                time.sleep(step)
            else:
                print "stop update..."
                break
    def quit(self):
        self.quitFlag=False

    def buildASerial(self, r, serialNo, tree):
        aSerial = ASerial(serialNo)
        duiZhen = tree.xpath('//table[@id="vsTable"]/tr[@data-vs]')
        for i, content in enumerate(duiZhen):
            extractTeam = [p.replace(u'\xa0', '') for p in content.xpath('td/span/a/text()')]
            print "extratTeam", r.encoding
            print extractTeam[1]
            teamPair = TeamPair(extractTeam[0], extractTeam[1])
            teamPair.no = content.xpath('td/text()')[0]
            teamPair.teamType =content.xpath('td[@class="league"]/a/text()')[0]

            urls = content.xpath('td/a/@href')
            teamPair.xinShuiUrl =urls[1]
            teamPair.ratioUrl = urls[3]
            ranks=content.xpath('td/span[@class="sp_pm"]/text()')
            if ranks:
                teamPair.homeTeamRank,teamPair.visitTeamRank =  re.search(r'\d+',ranks[0]).group() ,re.search(r'\d+',ranks[1]).group()

            print "teamrank:",teamPair.homeTeamRank,teamPair.visitTeamRank

            aSerial.teamPairs.append(teamPair)
        json_dumps = json.dumps(aSerial, default=lambda o: o.__dict__)
        print "afdafd:", json_dumps
        return aSerial

    def run(self):
        count=1
        while self.quitFlag:
            r = requests.get('http://trade.500.com/sfc/')
            r.encoding='gb2312'
            # r.encoding='utf-8'
            tree = html.fromstring(r.text)
            serialNo =tree.xpath('//span[contains(@id,"expect_tab")]/a[contains(@class,"on")]/@data-val')[0]
            print serialNo
            print 'ha haaha ha'
            base_find = dataBase.find(serialNo)
            if base_find is not None:
                print "[count: %d, time: %s] update serial:%s 's data.........   "% (count,time.strftime('%H:%M:%S',time.localtime(time.time())),serialNo)
                aSerial_old = dict2ASerial(base_find)
                for teamPair in aSerial_old.teamPairs:
                    teamPair.xinShui.build(teamPair.xinShuiUrl)
                    ratio= Ratio()
                    teamPair.willianRatio.append(ratio.build(teamPair.ratioUrl,u'威廉希尔'))
                    ratio= Ratio()
                    teamPair.ladbrokesRatio.append(ratio.build(teamPair.ratioUrl,u'Ladbrokes (立博)'))
                    ratio= Ratio()
                    teamPair.bet365Ratio.append(ratio.build(teamPair.ratioUrl,u'Bet365'))
                    ratio= Ratio()
                    teamPair.interRatio.append(ratio.build(teamPair.ratioUrl,u'Interwetten (英特)'))
                    ratio= Ratio()
                    teamPair.snaiRatio.append(ratio.build(teamPair.ratioUrl,u'SNAI'))

                dataBase.update(aSerial_old)
            else:
                print u'add a new Serial...'
                aSerial_new = self.buildASerial(r, serialNo, tree)
                dataBase.update(aSerial_new)

            self.wait()
            count=count+1

class ScrapyResult():
    def getResult(self):
        r = requests.get('http://kaijiang.500.com/sfc.shtml')
        r.encoding='gb2312'
        tree = html.fromstring(r.text)
        serialNo =tree.xpath('//span[@class="iSelectBox"]/a[@class="iSelect"]/text()')[0]
        print "latest opened serialNo:",serialNo
        noResults = dataBase.filterNoResult()
        for noResult in noResults:
            aSerial_old = dict2ASerial(noResult)
            print "begin write %s 's vs result..." %aSerial_old._id
            if int(aSerial_old._id) > int(serialNo):
                print "%s are not game over!" %aSerial_old._id
                continue
            r = requests.get('http://kaijiang.500.com/shtml/sfc/'+aSerial_old._id+'.shtml')
            r.encoding='gb2312'
            print 'http://kaijiang.500.com/shtml/sfc/'+aSerial_old._id+'.shtml'
            tree = html.fromstring(r.text)
            tmp =tree.xpath('//tr/td/span[@class="cfont5 "]/text()')
            print tmp
            for i, content in enumerate(aSerial_old.teamPairs):
                content.vsResult=tmp[i]

            dataBase.update(aSerial_old)
            print "end write %s 's vs result" %aSerial_old._id




