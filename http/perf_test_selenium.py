import time
import traceback
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import ConfigParser

import selenium_helper
import perf_utils

parser = argparse.ArgumentParser(description="GGRC Selenium perf test")
parser.add_argument('--chrome_path')
parser.add_argument('--out_dir')
parser.add_argument('--iterations', type=int, default=3)
args = parser.parse_args()
#print args.chrome_path
#exit()
#profilePath = '/Users/siarheis/Library/Application\ Support/Google/Chrome'
#> props default /usr/bin/chromedriver
#chromeDriverPath = '/Users/siarheis/utils/chromedriver'
#chromeDriverPath = args.chrome_path
out_dir = args.out_dir
iterations = args.iterations
# to props default 60
WAIT_TIMEOUT = 30
#to props def False
PERF_LOG = False
#to props default True
HEADLESS = True
SCREENSHOTS = True

config = ConfigParser.ConfigParser()
config.read('perf_test_selenium.ini')
user = config.get('login', 'user')
password = config.get('login', 'password')
#chromedriver_path
chromeDriverPath = config.get('config', 'chrome_driver')
#iterations = config.get('test', 'iterations')

baseURL = 'https://ggrc-perf.appspot.com/'
HOME_TITLE = 'GRC: My Work'
AUDIT_SEARCH = '2018: program_'
ASSESSMENT_NAME = 'ASSESSMENT-24643'

TR_HOME = '0001_Home'
TR_LOGIN = '0010_Login'
TR_LOGIN1 = '0008_LoginName'
TR_LOGIN2 = '0009_LoginPwd'
TR_LEFTPANEL = '0020_LeftPanel'
TR_COLLAPSEAUDIT = '0035_CollapseAudit'
TR_CLEARSEARCH = '0025_ClearSearch'
TR_SEARCH = '0030_Search'
TR_EXPANDAUDIT = '0040_ExpandAudit'
TR_OPENAUDIT = '0100_OpenAudit'
TR_OPENASSESSMENTS = '0110_OpenAssessments'
TR_SEARCHASSESSMENTS = '0120_SearchAssessments'
TR_ASSESSMENTOPENINAUDIT = '0200_AssessmenOpentInAudit'
TR_ASSESSMENTADDCOMMENTINAUDIT = '0210_AssessmentAddCommentInAudit'
TR_ASSESSMENTSELECTEMPTYLCAINAUDIT = '0215_AssessmentSelectEmptyLCAInAudit'
TR_ASSESSMENTSELECTYESLCAINAUDIT = '0220_AssessmentSelectYesLCAInAudit'
TR_ASSESSMENTSELECTNOLCAINAUDIT = '0230_AssessmentSelectNoLCAInAudit'
TR_ASSESSMENTADDCOMMENTLCAINAUDIT = '0240_AssessmentAddCommentLCAInAudit'
TR_ASSESSMENTCOMPLETEINAUDIT = '0250_AssessmentCompleteInAudit'
TR_ASSESSMENTVERIFYINAUDIT= '0260_AssessmentVerifyInAudit'
TR_ASSESSMENTMOVETOPROGRESSDIALOGINAUDIT = '0265_AssessmentMoveToProgressDialog'
TR_ASSESSMENTMOVETOPROGRESSINAUDIT = '0270_AssessmentMoveToProgress'
TR_ASSESSMENTMOVETOPROGRESSCONFIRMNAMEINAUDIT = '0275_AssessmentMoveToProgressConfirmName'
TR_ASSESSMENTOPEN = '0300_AssessmentOpen'
TR_ASSESSMENTADDCOMMENT = '0310_AssessmentAddComment'
TR_ASSESSMENTSELECTEMPTYLCA = '0325_AssessmentSelectEmptyLCA'
TR_ASSESSMENTSELECTYESLCA = '0330_AssessmentSelectYesLCA'
TR_ASSESSMENTSELECTNOLCA = '0330_AssessmentSelectNoLCA'
TR_ASSESSMENTADDCOMMENTLCA = '0340_AssessmentAddCommentLCA'
TR_ASSESSMENTCOMPLETE = '0350_AssessmentComplete'
TR_ASSESSMENTVERIFY = '0360_AssessmentVerify'
TR_ASSESSMENTMOVETOPROGRESSDIALOG = '0365_AssessmentMoveToProgressDialog'
TR_ASSESSMENTMOVETOPROGRESS = '0370_AssessmentMoveToProgress'
TR_ASSESSMENTMOVETOPROGRESSCONFIRMNAME = '0375_AssessmentMoveToProgressConfirmName'

perf_utils.saveTransactions(out_dir, 'results.csv')

for iter in range(1, iterations+1):
  options = webdriver.ChromeOptions()
  options.add_argument('--incognito')
  if (HEADLESS):
    options.add_argument('--headless')
  options.add_argument('--disable-extensions')
  options.add_argument('--window-size=1024x768')

  driver = webdriver.Chrome(chromeDriverPath,
                              chrome_options=options,
                              )

  wait = WebDriverWait(driver, WAIT_TIMEOUT)

  if (SCREENSHOTS):
    perf_utils.saveScreenshots(driver)

  perf_utils.startTransaction(TR_HOME)
  try:
    driver.get(baseURL)
    result = True
  except:
    perf_utils.saveError(TR_HOME, traceback.format_exc())
    result = False
  finally:
    perf_utils.endTransaction(TR_HOME, result)

  if (HEADLESS):
    CSS_EMAIL = 'input#Email'
    CSS_EMAILNEXT = 'input#next'
    CSS_PWD = 'input#Passwd'
    CSS_PWDNEXT = 'input#signIn'
  else:
    CSS_EMAIL = 'input#identifierId'
    CSS_EMAILNEXT = 'div#identifierNext'
    CSS_PWD = 'input[name="password"]'
    CSS_PWDNEXT = 'div#passwordNext'

  elem = driver.find_element_by_link_text('Login')

  perf_utils.startTransaction(TR_LOGIN1)
  try:
    elem.click()
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_EMAIL)))
    result = True
  except:
    perf_utils.saveError(TR_LOGIN1, traceback.format_exc())
    result = False
  finally:
    perf_utils.endTransaction(TR_LOGIN1, result)

  elem.send_keys(user)
  elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_EMAILNEXT)))
  try:
    perf_utils.startTransaction(TR_LOGIN2)
    elem.click()
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_PWD)))
    result = True
  except:
    perf_utils.saveError(TR_LOGIN2, traceback.format_exc())
    result = False
  finally:
    perf_utils.endTransaction(TR_LOGIN2, result)

  elem.send_keys(password)
  elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_PWDNEXT)))
  perf_utils.startTransaction(TR_LOGIN)
  try:
    elem.click()
    result = True
  except:
    perf_utils.saveError(TR_LOGIN, traceback.format_exc())
    result = False
  finally:
    perf_utils.endTransaction(TR_LOGIN, result)

  #print driver.page_source.encode('utf-8')
  #elem = driver.find_element(By.CSS_SELECTOR, 'div[id="passwordNext"]')

  #elem = driver.find_element(By.CSS_SELECTOR, '.simple-modal.release-notes')
  #print 'notes'
  #elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'release-notes__version-block > button')))
  #driver.save_screenshot(TR_LOGIN + '.png'
  """
  perf_utils.startTransaction(TR_LEFTPANEL)
  try:
    elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[data-original-title="Programs"]')))
    result = True
  except:
    perf_utils.saveError(TR_LEFTPANEL, traceback.format_exc())
    result = False
  finally:
    perf_utils.endTransaction(TR_LEFTPANEL, result)
  """
  driver.quit()

  #print elem.text
  #elem.click()
  #release-notes__version-block > button
  #time.sleep(10)
  #print driver.title.encode('utf-8')

perf_utils.endTest()
perf_utils.processResults(
    out_dir + '/' + 'results.csv', out_dir + '/' + 'summary.csv')
