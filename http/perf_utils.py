import time
import csv
import sys
from selenium import webdriver
from collections import OrderedDict

transactions = []
screenshots = False
writeToFile = False
path = ''
fn = ''
driver = ''

def startTest ():
  0

def saveScreenshots (drv):
  global screenshots
  global driver
  driver = drv
  screenshots = True

def saveTransactions (fpath, filename):
  global path
  global fn
  global writeToFile
  path = fpath
  fn = open(path+'/'+filename, 'a')
  writeToFile = True

def endTest ():
  if (writeToFile):
    fn.close()

def saveError(trName,exc):
  print '-'*80
  print trName + ' has FAILED!'
  print '-'*80
  print exc
  print '-'*80

def startTransaction (trName):
  print 'Start: ' + trName
  start = int(time.time() * 1000)
  transactions.append({'Name' : trName, 'Start': start})

def endTransaction (trName, result):
  global path
  end = int(time.time() * 1000)
  found = False
  for i in range(len(transactions), 0, -1):
    if (transactions[i-1]['Name'] == trName):
      transactions[i-1]['Result'] = result
      found = True
      transactions[i-1]['End'] = end
      start = transactions[i-1]['Start']
      transactions[i-1]['Duration'] = (end - start)
#      print writeToFile
      if (writeToFile):
        fn.write(
          str(start) + ',' +
          '"' + transactions[i-1]['Name'] + '"' + ',' +
          str(transactions[i-1]['Duration']) + ',' +
          str(result) +
          '\n')
      print transactions[i-1]
      break
  if (screenshots):
    driver.get_screenshot_as_file(path + '/' + trName + '-' + str(start) +
                                  '.scr' + '.png')
    #driver.get_screenshot_as_base64(trName + '.scr' + '.txt')
  if (found):
    print 'End: ' + trName
  else:
    print 'Appropriate startTransaction for ' + trName + ' not found'
  sys.stdout.flush()

def processResults(inFile, outFile):
  transactionResults = OrderedDict()
  with open(inFile, 'r') as fn:
    csv_reader = csv.reader(fn)
    for row in csv_reader:
      if transactionResults.has_key(row[1]):
        transactionResults[row[1]]['time'].append(int(row[2]))
        transactionResults[row[1]]['res'].append(row[3])
      else:
        transactionResults[row[1]] = OrderedDict()
        transactionResults[row[1]]['time'] = [int(row[2]),]
        transactionResults[row[1]]['res'] = [row[3], ]
  with open(outFile, 'w') as fn:
    for tr in transactionResults:
      sumt = sum(transactionResults[tr]['time'])
      mint = min(transactionResults[tr]['time'])
      maxt = max(transactionResults[tr]['time'])
      num = len(transactionResults[tr]['time'])
      numf = transactionResults[tr]['res'].count('False')
      avgt = sumt / num
      fn.write('"' + tr + '"' + ',' + str(num) + ',' + str(numf)+ ',' +
        str(mint) + ',' + str(avgt) + ',' + str(maxt) + '\n')

def processResultsJmeter(inFile, outFile):
  transactionResults = OrderedDict()
  with open(inFile, 'r') as fn:
    next(fn)
    csv_reader = csv.reader(fn)
    for row in csv_reader:
      if transactionResults.has_key(row[2]):
        transactionResults[row[2]]['time'].append(int(row[1]))
        transactionResults[row[2]]['res'].append(row[7])
      else:
        transactionResults[row[2]] = OrderedDict()
        transactionResults[row[2]]['time'] = [int(row[1]),]
        transactionResults[row[2]]['res'] = [row[7], ]
  with open(outFile, 'w') as fn:
    for tr in transactionResults:
      sumt = sum(transactionResults[tr]['time'])
      mint = min(transactionResults[tr]['time'])
      maxt = max(transactionResults[tr]['time'])
      num = len(transactionResults[tr]['time'])
      numf = transactionResults[tr]['res'].count('false')
      avgt = sumt / num
      fn.write('"' + tr + '"' + ',' + str(num) + ',' + str(numf)+ ',' +
        str(mint) + ',' + str(avgt) + ',' + str(maxt) + '\n')
