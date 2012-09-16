#!/usr/bin/env python

import time
import os
from flask import Flask, render_template, make_response, request, redirect, session, url_for

app = Flask(__name__)
app.config.from_pyfile('settings.config')

def getTimestamp():
  return str(int(time.time()))


def generateDensityMap(size):
  with open('density.txt', 'w') as f:
    for row in xrange(size):
      for col in xrange(18):
        f.write("%05d " % int(random.gauss(0.5, 0.1) * 100))
      f.write('\n')


@app.route('/')
def intro():
  return render_template('intro.html')


LevelOnePass = 'twasTheNightBeforeChristmas'
@app.route('/levelone', methods=['GET', 'POST'])
def level_one():
  if 'start' not in session:
    session['start'] = getTimestamp()

  badPass = False
  if request.method == 'POST':
    if request.form['password'] == LevelOnePass:
      session['passedLevelOne'] = getTimestamp()
      return redirect(url_for('level_two'))
    else:
      badPass = True
    
  resp = make_response(render_template('levelone.html', badPass=badPass))
  resp.headers['X-Signpost-password'] = LevelOnePass
  return resp


LevelTwoAnswer = '772' # 147 + 156 + 242 + 156 + 71
@app.route('/leveltwo', methods=['GET', 'POST'])
def level_two():
  if 'passedLevelOne' not in session:
    session['triedToLevelHop'] = getTimestamp()
    return redirect(url_for('level_one'))

  badPass = False
  if request.method == 'POST':
    if request.form['password'].strip() == LevelTwoAnswer:
      session['passedLevelTwo'] = getTimestamp()
      return redirect(url_for('complete'))
    else:
      badPass = True
  
  return render_template('leveltwo.html', badPass=badPass)


@app.route('/complete')
def complete():
  if 'passedLevelTwo' not in session:
    session['triedToLevelHop'] = getTimestamp()
    return redirect(url_for('level_one'))

  startTime = int(session['start'])
  finishOne = int(session['passedLevelOne'])
  finishTwo = int(session['passedLevelTwo'])

  completionCode = "%s-%s-%s" % (finishOne - startTime, finishTwo - finishOne, 1 if 'triedToLevelHop' in session else 0)
  return render_template('complete.html', completionCode=completionCode)


if __name__ == '__main__':
  port = int(os.environ.get('PORT', app.config['PORT']))
  app.run(host='0.0.0.0', port=port)
