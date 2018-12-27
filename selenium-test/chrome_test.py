import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import selenium_helper
import perf_utils

profilePath = '/Users/siarheis/Library/Application\ Support/Google/Chrome'
chromeDriverPath = '/Users/siarheis/utils/chromedriver'
WAIT_TIMEOUT = 60
PERF_LOG = False

baseURL = 'https://ggrc-perf.appspot.com/'
HOME_TITLE = 'GRC: My Work'
AUDIT_SEARCH = '2018: program_'
ASSESSMENT_NAME = 'ASSESSMENT-24643'

perf_utils.saveTransactions('results.csv')

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + profilePath)
if (PERF_LOG):
  caps = DesiredCapabilities.CHROME
  caps['loggingPrefs'] = {'performance': 'ALL',} # 'browser': 'ALL', 'driver': 'ALL'}
  driver = webdriver.Chrome(chromeDriverPath,
                            desired_capabilities=caps,
                            chrome_options=options,
#                          service_args=["--verbose", "--log-path=/Users/siarheis/utils/chr.log"],
                            )
  driver.command_executor._commands.update({
     'getAvailableLogTypes': ('GET', '/session/$sessionId/log/types'),
     'getLog': ('POST', '/session/$sessionId/log')})
  print 'Available log types:', driver.execute('getAvailableLogTypes')['value']
else:
  driver = webdriver.Chrome(chromeDriverPath,
                            chrome_options=options,
                            )

wait = WebDriverWait(driver, WAIT_TIMEOUT)

TR_HOME = '0001_Home'
TR_LOGIN = '0010_Login'
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

perf_utils.startTransaction(TR_HOME)
driver.get(baseURL)
perf_utils.endTransaction(TR_HOME)

# start login
elem = driver.find_element_by_link_text('Login')
perf_utils.startTransaction(TR_LOGIN)
elem.click()

#login check
if (driver.title == HOME_TITLE):
 time.sleep(0)

else:
  print('Need login!')
  driver.save_screenshot('login.png')
  time.sleep(300)
# end check login

perf_utils.endTransaction(TR_LOGIN)
#end login

perf_utils.startTransaction(TR_LEFTPANEL)
elem = driver.find_element(By.CSS_SELECTOR, '.lhn-trigger')
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="lhs"]/div[1]/ul/li[1]/a/span/small/span')))
numberOfPrograms = elem.text
perf_utils.endTransaction(TR_LEFTPANEL)

elem = driver.find_element(By.CSS_SELECTOR, '[data-model-name="Audit"]>a[data-object-singular="Audit"]')
if (elem.get_attribute('class') == u'programs list-toggle active'):
  perf_utils.startTransaction(TR_COLLAPSEAUDIT)
  elem = driver.find_element(By.CSS_SELECTOR, 'li[data-model-name="Audit"]>a[data-object-singular="Audit"]>span[class="lhs-item lhs-item-long"]')
  elem.click()
  elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'li[data-model-name="Audit"]>div>ul')))
  perf_utils.endTransaction(TR_COLLAPSEAUDIT)

elem = driver.find_element_by_class_name('widgetsearch')
if (elem.get_attribute('value') != u''):
  perf_utils.startTransaction(TR_CLEARSEARCH)
  elem = driver.find_element_by_css_selector('#lhs > form > div > div > a')
  elem.click()
  elem = wait.until(selenium_helper.element_text_has_changed((By.XPATH, '//*[@id="lhs"]/div[1]/ul/li[1]/a/span/small/span'), numberOfPrograms))
  numberOfPrograms = elem.text
  perf_utils.endTransaction(TR_CLEARSEARCH)

elem = driver.find_element_by_class_name('widgetsearch')
elem.send_keys(AUDIT_SEARCH)
perf_utils.startTransaction(TR_SEARCH)
elem = driver.find_element_by_class_name('widgetsearch-submit')
elem.click()
elem = wait.until(selenium_helper.element_text_has_changed((By.XPATH, '//*[@id="lhs"]/div[1]/ul/li[1]/a/span/small/span'), numberOfPrograms))
perf_utils.endTransaction(TR_SEARCH)

elem = driver.find_element(By.CSS_SELECTOR, 'li[data-model-name="Audit"]>a[data-object-singular="Audit"]>span[class="lhs-item lhs-item-long"]')
perf_utils.startTransaction(TR_EXPANDAUDIT)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/audits/4567"]')))
perf_utils.endTransaction(TR_EXPANDAUDIT)

perf_utils.startTransaction(TR_OPENAUDIT)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.top-inner-nav > div.object-nav > div > div > ul > li > a[href="/audits/4567#!summary"]')))
perf_utils.endTransaction(TR_OPENAUDIT)

elem = driver.find_element(By.CSS_SELECTOR, 'div.top-inner-nav > div.object-nav > div > div > ul > li > a[href="/audits/4567#!assessment"]')
perf_utils.startTransaction(TR_OPENASSESSMENTS)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'tree-view > tree-item')))
perf_utils.endTransaction(TR_OPENASSESSMENTS)

elem = driver.find_element(By.CSS_SELECTOR, '.tree-filter__input')
elem.send_keys(ASSESSMENT_NAME)
elem = driver.find_element(By.CSS_SELECTOR, '.tree-filter__actions')
perf_utils.startTransaction(TR_SEARCHASSESSMENTS)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.tree-spinner')))
elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.tree-spinner')))
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'tree-view > tree-item')))
perf_utils.endTransaction(TR_SEARCHASSESSMENTS)

elem = driver.find_element(By.CSS_SELECTOR, 'tree-view > tree-item > div > div > .flex-box')
perf_utils.startTransaction(TR_ASSESSMENTOPENINAUDIT)
elem.click()
#elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'spinner.info-pane__section-title-icon')))
#elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'spinner.info-pane__section-title-icon')))
#elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'spinner')))
#elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'spinner.spinner-wrapper.active')))
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.assessment-controls__extra-controls > div > object-list > div > div.object-list__item')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'comment-input > rich-text > div > div > .ql-editor.ql-blank')))
perf_utils.endTransaction(TR_ASSESSMENTOPENINAUDIT)

elem = driver.find_element(By.CSS_SELECTOR, 'a[data-object-id]')
assessmentId = elem.get_attribute('data-object-id')

#elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'comment-input > rich-text > div > div > .ql-editor.ql-blank')))
elem = driver.find_element(By.CSS_SELECTOR, 'comment-input > rich-text > div > div > .ql-editor.ql-blank')
elem.send_keys(ASSESSMENT_NAME + str(time.time()))
elem = driver.find_element(By.CSS_SELECTOR, 'comment-add-button')
perf_utils.startTransaction(TR_ASSESSMENTADDCOMMENTINAUDIT)
elem.click()
#elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.comment-add-form__toolbar-checkbox')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTADDCOMMENTINAUDIT)

select = Select(driver.find_element(By.CSS_SELECTOR, 'dropdown-form-field > div > dropdown > select'))
elem = select.first_selected_option
if (elem.get_attribute('value') != u''):
  perf_utils.startTransaction(TR_ASSESSMENTSELECTEMPTYLCAINAUDIT)
  select.select_by_value('')
  elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
  elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
  elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
  perf_utils.endTransaction(TR_ASSESSMENTSELECTEMPTYLCAINAUDIT)

perf_utils.startTransaction(TR_ASSESSMENTSELECTYESLCAINAUDIT)
select.select_by_value('yes')
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTSELECTYESLCAINAUDIT)

perf_utils.startTransaction(TR_ASSESSMENTSELECTNOLCAINAUDIT)
select.select_by_value('no')
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'form.simple-modal__body > div > comment-input > rich-text > div > div > .ql-editor.ql-blank')))
perf_utils.endTransaction(TR_ASSESSMENTSELECTNOLCAINAUDIT)

elem.send_keys(ASSESSMENT_NAME + str(time.time()))
elem = driver.find_element(By.CSS_SELECTOR, '.simple-modal__toolbar > comment-add-button > button')
perf_utils.startTransaction(TR_ASSESSMENTADDCOMMENTLCAINAUDIT)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTADDCOMMENTLCAINAUDIT)

action = ActionChains(driver)

elem = driver.find_element(By.CSS_SELECTOR, '.nav.nav-tabs > .active')
action.move_to_element(elem).perform()
elem = driver.find_element(By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')
perf_utils.startTransaction(TR_ASSESSMENTCOMPLETEINAUDIT)
elem.click()
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTCOMPLETEINAUDIT)

elem = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-small.btn-green.object-state-toolbar__item')
perf_utils.startTransaction(TR_ASSESSMENTVERIFYINAUDIT)
elem.click()
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTVERIFYINAUDIT)

elem = driver.find_element(By.CSS_SELECTOR, 'base-inline-control-title > div')
action.move_to_element(elem).perform()
elem = driver.find_element(By.CSS_SELECTOR, 'base-inline-control-title > div > div > action-toolbar-control > div')
perf_utils.startTransaction(TR_ASSESSMENTMOVETOPROGRESSDIALOGINAUDIT)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.modal.hide.undefined.in.ggrc_controllers_modals  > .modal-footer > .row-fluid > div > .confirm-buttons')))
perf_utils.endTransaction(TR_ASSESSMENTMOVETOPROGRESSDIALOGINAUDIT)

elem = driver.find_element(By.CSS_SELECTOR,
                           '.modal.hide.undefined.in.ggrc_controllers_modals  > .modal-footer > .row-fluid > div > .confirm-buttons > a')
perf_utils.startTransaction(TR_ASSESSMENTMOVETOPROGRESSINAUDIT)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTMOVETOPROGRESSINAUDIT)

elem = driver.find_element(By.CSS_SELECTOR, '.fa.fa-check')
perf_utils.startTransaction(TR_ASSESSMENTMOVETOPROGRESSCONFIRMNAMEINAUDIT)
elem.click()
perf_utils.endTransaction(TR_ASSESSMENTMOVETOPROGRESSCONFIRMNAMEINAUDIT)

elem = driver.find_element(By.CSS_SELECTOR, '.info-pane-utility > div .details-wrap')
elem.click()
elem = driver.find_element(By.CSS_SELECTOR, '.details-wrap > .dropdown-menu > li > a[href="/assessments/' + assessmentId + '"]')
perf_utils.startTransaction(TR_ASSESSMENTOPEN)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.assessment-controls__extra-controls > div > object-list > div > div.object-list__item')))
perf_utils.endTransaction(TR_ASSESSMENTOPEN)

elem = driver.find_element(By.CSS_SELECTOR, 'comment-input > rich-text > div > div > .ql-editor')
elem.send_keys(ASSESSMENT_NAME + str(time.time()))
elem = driver.find_element(By.CSS_SELECTOR, 'comment-add-button')
perf_utils.startTransaction(TR_ASSESSMENTADDCOMMENT)
elem.click()
#elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.comment-add-form__toolbar-checkbox')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTADDCOMMENT)

select = Select(driver.find_element(By.CSS_SELECTOR, 'dropdown-form-field > div > dropdown > select'))

perf_utils.startTransaction(TR_ASSESSMENTSELECTEMPTYLCA)
select.select_by_value('')
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTSELECTEMPTYLCA)

perf_utils.startTransaction(TR_ASSESSMENTSELECTYESLCA)
select.select_by_value('yes')
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTSELECTYESLCA)

perf_utils.startTransaction(TR_ASSESSMENTSELECTNOLCA)
select.select_by_value('no')
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'form.simple-modal__body > div > comment-input > rich-text > div > div > .ql-editor.ql-blank')))
perf_utils.endTransaction(TR_ASSESSMENTSELECTNOLCA)

elem.send_keys(ASSESSMENT_NAME + str(time.time()))
elem = driver.find_element(By.CSS_SELECTOR, '.simple-modal__toolbar > comment-add-button > button')
perf_utils.startTransaction(TR_ASSESSMENTADDCOMMENTLCA)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTADDCOMMENTLCA)

elem = driver.find_element(By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')
perf_utils.startTransaction(TR_ASSESSMENTCOMPLETE)
elem.click()
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTCOMPLETE)

elem = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-small.btn-green.object-state-toolbar__item')
perf_utils.startTransaction(TR_ASSESSMENTVERIFY)
elem.click()
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTVERIFY)

action = ActionChains(driver)
elem = driver.find_element(By.CSS_SELECTOR, 'base-inline-control-title > div')
action.move_to_element(elem).perform()
elem = driver.find_element(By.CSS_SELECTOR, 'base-inline-control-title > div > div > action-toolbar-control > div')
perf_utils.startTransaction(TR_ASSESSMENTMOVETOPROGRESSDIALOG)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.modal.hide.undefined.in.ggrc_controllers_modals  > .modal-footer > .row-fluid > div > .confirm-buttons')))
perf_utils.endTransaction(TR_ASSESSMENTMOVETOPROGRESSDIALOG)

elem = driver.find_element(By.CSS_SELECTOR,
                           '.modal.hide.undefined.in.ggrc_controllers_modals  > .modal-footer > .row-fluid > div > .confirm-buttons > a')
perf_utils.startTransaction(TR_ASSESSMENTMOVETOPROGRESS)
elem.click()
elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'loading-status > spinner')))
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.object-state-toolbar > .object-state-toolbar__item')))
perf_utils.endTransaction(TR_ASSESSMENTMOVETOPROGRESS)

elem = driver.find_element(By.CSS_SELECTOR, '.fa.fa-check')
perf_utils.startTransaction(TR_ASSESSMENTMOVETOPROGRESSCONFIRMNAME)
elem.click()
perf_utils.endTransaction(TR_ASSESSMENTMOVETOPROGRESSCONFIRMNAME)

if (PERF_LOG):
  for entry in driver.get_log('performance'):
    print entry
  print 'Profiler log:', driver.execute('getLog', {'type': 'performance'})['value']
driver.quit()

perf_utils.endTest()
perf_utils.processResults('results.csv', 'summary.csv')

#perf_utils.endTest()
#driver.quit()
#perf_utils.processResults('results.csv', 'summary.csv')
#exit()
