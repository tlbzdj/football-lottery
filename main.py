from fetch.teamdata import ScrapyModel, ScrapyResult

__author__ = 'Administrator'

myModel = ScrapyModel()
myModel.start()

result=ScrapyResult()
result.getResult()
while True:
    myInput = raw_input('if you want quit anyway,please input quit: ')
    if myInput =='quit':
        myModel.quit()
        break

myModel.join()
print "over!!!!!"

