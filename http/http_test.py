from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import Response
import subprocess
import os
import time
from time import sleep
import csv
from collections import OrderedDict

import calendar

app = Flask(__name__)

@app.after_request
def add_header(r):
  r.headers['Cache-Control'] = 'no-cahce, no-store, must-revalidate, public, max-age=0'
  r.headers['Pragma'] = 'no-cache'
  r.headers['Expires'] = '0'
  return r

@app.route('/')
def perf_test():
  selenium_msg = []
  jmeter_msg = []
  run_filename_selenium = app.root_path + '/selenium/' + '.running'
  run_filename_jmeter = app.root_path + '/jmeter/' + '.running'
  running_selenium = os.path.isfile(run_filename_selenium)
  running_jmeter = os.path.isfile(run_filename_jmeter)
  if (running_selenium):
    selenium_msg.append('Test was started %s' %
                        time.ctime(os.path.getmtime(run_filename_selenium)))
    selenium_msg.append('Test is running for %s' %
                        time.strftime('%H:%M:%S',
                                      time.localtime(time.mktime(time.gmtime()) -
                                                     os.path.getmtime(run_filename_selenium))))
    selenium_results_url = '/selenium/running'
    selenium_results_text = 'Logs output'
  else:
    dirnames = []
    for (_, dirnames, _) in os.walk(app.root_path + '/selenium/'):
      dirnames.sort(reverse=True)
      break
    selenium_msg = []
    selenium_results_url = '/selenium/results/' + dirnames[0]
    selenium_results_text = dirnames[0]

  if (running_jmeter):
    jmeter_msg.append('Test was started %s' %
                        time.ctime(os.path.getmtime(run_filename_jmeter)))
    jmeter_msg.append('Test is running for %s' %
                        time.strftime('%H:%M:%S',
                                      time.localtime(
                                        time.mktime(time.gmtime()) -
                                        os.path.getmtime(
                                          run_filename_jmeter))))
    jmeter_results_url = '/jmeter/running'
    jmeter_results_text = 'Logs output'
  else:
    dirnames = []
    for (_, dirnames, _) in os.walk(app.root_path + '/jmeter/'):
      dirnames.sort(reverse=True)
      break
    jmeter_msg = []
    jmeter_results_url = '/jmeter/results/' + dirnames[0]
    jmeter_results_text = dirnames[0]
  return render_template('perf_test.html', name='GGRC Performance POC',
                         running_selenium=running_selenium,
                         selenium_msg=selenium_msg,
                         running_jmeter = running_jmeter,
                         jmeter_msg=jmeter_msg,
                         selenium_results_url = selenium_results_url,
                         selenium_results_text = selenium_results_text,
                         jmeter_results_url = jmeter_results_url,
                         jmeter_results_text = jmeter_results_text)
  cmd = [' /Users/siarheis/venv/bin/python',
         'perf_test_selenium.py',
         '--out_dir=./20181201',
         '--iterations=3']
  #/Users/siarheis/venv/bin/python perf_test_selenium.py --chrome_path=/Users/siarheis/utils/chromedriver --out_dir=./20181201 --iterations=3
  p = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE
  )
  out,err = p.communicate()
  return render_template('perf_test.html', name='GGRC Performance POC', out=out, err=err)

@app.route('/info')
def info():
  str = 'app.root_path:' + app.root_path + '\n'
  return str

@app.route('/run_selenium', methods=['POST'])
def run_selenium_test():
#  print request.form
  print request.form.get('url')
  print request.form.get('iter')
  cmd = [app.root_path + '/run_test_selenium.sh',
         request.form.get('iter')]
  p = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE
  )
#  out,err = p.communicate()
  time.sleep(1)
  return redirect('/', code=303)

@app.route('/run_jmeter', methods=['POST'])
def run_jmeter_test():
#  print request.form
  print request.form.get('url')
  print request.form.get('iter')
  cmd = [app.root_path + '/run_test_jmeter.sh',
         request.form.get('iter')]
  p = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE
  )
  time.sleep(1)
  return redirect('/', code=303)

@app.route('/selenium/log')
def show_selenium_log():
  try:
    with open(app.root_path + '/selenium/.running.test/output.log', 'r') as fn:
      msg = fn.read()
    return Response(msg,mimetype='text/plain')
  except:
    return redirect('/', code=303)

@app.route('/jmeter/log')
def show_jmeter_log():
  try:
    with open(app.root_path + '/jmeter/.running.test/output.log', 'r') as fn:
      msg = fn.read()
    return Response(msg,mimetype='text/plain')
  except:
    return redirect('/', code=303)

@app.route('/selenium/results')
def show_selenium_all_results():
  for (_, dirnames, _) in os.walk(app.root_path + '/selenium/'):
    dirnames.sort(reverse=True)
    break
  msg = ''
  for dir in dirnames:
    if dir != 'running.test':
      msg += '<a href="/selenium/results/%s">%s</a><br>\n' % (dir, dir)
  return render_template('all_results.html', msg = msg)

@app.route('/jmeter/results')
def show_jmeter_all_results():
  for (_, dirnames, _) in os.walk(app.root_path + '/jmeter/'):
    dirnames.sort(reverse=True)
    break
  msg = ''
  for dir in dirnames:
    if dir != 'running.test':
      msg += '<a href="/jmeter/results/%s">%s</a><br>\n' % (dir, dir)
  return render_template('all_results.html', msg = msg)

@app.route('/selenium/results/<res_dir>')
def show_selenium_last_results(res_dir):
  transactionResults = OrderedDict()
  inFile = app.root_path + '/selenium/' + '.sla'
  with open(inFile, 'r') as fn:
    csv_reader = csv.reader(fn)
    for row in csv_reader:
        transactionResults[row[0]] = OrderedDict()
        transactionResults[row[0]]['sla'] = int(row[1])
  inFile = app.root_path + '/selenium/' + res_dir + '/' +'summary.csv'
  with open(inFile, 'r') as fn:
    csv_reader = csv.reader(fn)
    for row in csv_reader:
        transactionResults[row[0]]['res'] = row[1:]
  row = ''
  for tr, res in transactionResults.items():
    (p,f,min,avg,max) = res['res']
    row += '<tr>'
    row += '<td>%s</td>' % tr
    row += '<td align=right>%s</td>' % res['sla']
    row += '<td align=right>%s</td>' % p
    if (int(f) == 0):
      row += '<td align=right>%s</td>' % f
    else:
      row += '<td align=right bgcolor=#FF8080><b>%s<b></td>' % f
    row += '<td align=right>%s</td>' % min
    if ((int(res['sla']) > 0) and (int(avg) > int(res['sla']))):
      row += '<td align=right bgcolor=#FF8080><b>%s<b></td>' % avg
    else:
      row += '<td align=right bgcolor=#80FF80>%s</td>' % avg
    row += '<td align=right>%s</td>' % max
    row += '</tr>' + '\n'
  return render_template('results.html',
                         res_dir=res_dir,
                         rows = row,
                         transactions=transactionResults)

@app.route('/jmeter/results/<res_dir>')
def show_jmeter_last_results(res_dir):
  transactionResults = OrderedDict()
  inFile = app.root_path + '/jmeter/' + '.sla'
  with open(inFile, 'r') as fn:
    csv_reader = csv.reader(fn)
    for row in csv_reader:
        transactionResults[row[0]] = OrderedDict()
        transactionResults[row[0]]['sla'] = int(row[1])
  inFile = app.root_path + '/jmeter/' + res_dir + '/' +'summary.csv'
  with open(inFile, 'r') as fn:
    csv_reader = csv.reader(fn)
    for row in csv_reader:
        transactionResults[row[0]]['res'] = row[1:]
  row = ''
  for tr, res in transactionResults.items():
    (p,f,min,avg,max) = res['res']
    row += '<tr>'
    row += '<td>%s</td>' % tr
    row += '<td align=right>%s</td>' % res['sla']
    row += '<td align=right>%s</td>' % p
    if (int(f) == 0):
      row += '<td align=right>%s</td>' % f
    else:
      row += '<td align=right bgcolor=#FF8080><b>%s<b></td>' % f
    row += '<td align=right>%s</td>' % min
    if ((int(res['sla']) > 0) and (int(avg) > int(res['sla']))):
      row += '<td align=right bgcolor=#FF8080><b>%s<b></td>' % avg
    else:
      row += '<td align=right bgcolor=#80FF80>%s</td>' % avg
    row += '<td align=right>%s</td>' % max
    row += '</tr>' + '\n'
  return render_template('results.html',
                         res_dir=res_dir,
                         rows = row,
                         transactions=transactionResults)
