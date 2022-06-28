from app import app
from flask import render_template, request, session, redirect, url_for
from math import sqrt

returns = {str(i+1): [0.05, False] for i in range(35)}
logIns = {'ACG': 'ACG1317', 'acg': 'ACG1317'}

marketReturns = [43.81, -8.30, -25.12, -43.84, -8.64, 49.98, -1.19, 46.74, 31.94, -35.34, 29.28, -1.10, -10.67, -12.77, 19.17, 25.06, 19.03, 35.82, -8.43, 5.20, 5.70, 18.30, 30.81, 23.68, 18.15,
                 -1.21, 52.56, 32.60, 7.44, -10.46, 43.72, 12.06, 0.34, 26.64, -8.81, 22.61, 16.42, 12.40, -
                 9.97, 23.80, 10.81, -8.24, 3.56, 14.22, 18.76, -
                 14.31, -25.90, 37.00, 23.83, -6.98,
                 6.51, 18.52, 31.74, -4.70, 20.42, 22.34, 6.15, 31.24, 18.49, 5.81, 16.54, 31.48, -
                 3.06, 30.23, 7.49, 9.97, 1.33, 37.20, 22.68, 33.10, 28.34, 20.89, -
                 9.03, -11.85, -21.97, 28.36,
                 10.74, 4.83, 15.61, 5.48, -36.55, 25.94, 14.82, 2.10, 15.89, 32.15, 13.52, 1.38, 11.77, 21.61, -4.23, 31.21, 18.02, 28.47]


bondReturns = [0.84, 4.20, 4.54, -2.56, 8.79, 1.86, 7.96, 4.47, 5.02, 1.38, 4.21, 4.41, 5.40, -2.02, 2.29, 2.49, 2.58, 3.80, 3.13, 0.92, 1.95, 4.66, 0.43, -0.30, 2.27, 4.14, 3.29, -1.34,
               -2.26, 6.80, -2.10, -2.65, 11.64, 2.06, 5.69, 1.68, 3.73, 0.72, 2.91, -1.58, 3.27, -
               5.01, 16.75, 9.79, 2.82, 3.66, 1.99, 3.61, 15.98, 1.29, -
               0.78, 0.67, -2.99, 8.20, 32.81,
               3.20, 13.73, 25.71, 24.28, -4.96, 8.22, 17.69, 6.24, 15.00, 9.36, 14.21, -
               8.04, 23.48, 1.43, 9.94, 14.92, -
               8.25, 16.66, 5.57, 15.12, 0.38, 4.49, 2.87, 1.96, 10.21, 20.10,
               -11.12, 8.46, 16.04, 2.97, -9.10, 10.75, 1.28, 0.69, 2.80, -0.02, 9.64, 11.33, -4.42]


def returnStreams(market, bond, x, y):
    masterList = []
    for i in range(len(market)-34):
        masterList.append([(market[i]*x)+(bond[i]*y) for i in range(i, i+35)])
    return(masterList)


returnCombinations = {'market': returnStreams(marketReturns, bondReturns, 1, 0), 'bonds': returnStreams(marketReturns, bondReturns, 0, 1), '90M10B': returnStreams(marketReturns, bondReturns, 0.9, 0.1), '80M20B': returnStreams(marketReturns, bondReturns, 0.8, 0.2), '70M30B': returnStreams(marketReturns, bondReturns, 0.7, 0.3), '60M40B': returnStreams(
    marketReturns, bondReturns, 0.6, 0.4), '50M50B': returnStreams(marketReturns, bondReturns, 0.5, 0.5), '40M60B': returnStreams(marketReturns, bondReturns, 0.4, 0.6), '30M70B': returnStreams(marketReturns, bondReturns, 0.3, 0.7), '20M80B': returnStreams(marketReturns, bondReturns, 0.2, 0.8), '10M90B': returnStreams(marketReturns, bondReturns, 0.1, 0.9)}


@app.route('/', methods=['GET', 'POST'])
def home():

    session['loggedIn'] = False

    if request.method == 'POST':
        if request.form['username'] in logIns:
            if request.form['password'] == logIns[request.form['username']]:
                session['loggedIn'] = True
                return redirect(url_for('data'))

    return render_template('login.html')


@app.route('/data', methods=['POST', 'GET'])
def data():

    if session['loggedIn'] == True:

        if request.method == 'POST' and 'Starting Year' in request.form and request.form['Starting Year'] != '':
            try:
                if int(request.form['Starting Year']) > 1927 and int(request.form['Starting Year']) < 1988:
                    session['start'] = int(request.form['Starting Year'])

                for i in range(35):

                    if session['portfolio'][2] == 'a':
                        returns[str(i+1)] = [0.05, False]

                    elif session['portfolio'][2] == '0':

                        if session['portfolio'][5] == 'E':
                            returns[str(
                                i+1)] = [((marketReturns[(session['start']-1928)+i]/100)), False]
                        else:
                            returns[str(
                                i+1)] = [((bondReturns[(session['start']-1928)+i]/100)), False]

                    else:
                        returns[str(i+1)] = [((marketReturns[(session['start']-1928)+i]/100)*(int(session['portfolio'][0])/10)) + (
                            (bondReturns[(session['start']-1928)+i]/100)*(int(session['portfolio'][12])/10)), False]

                session['window'] = str(
                    session['start']) + '-' + str(session['start']+34)

            except:
                pass

        def returnChanger(x, y):
            for i in range(35):
                try:
                    returns[str(i+1)] = [((marketReturns[(session['start']-1928)+i]/100)
                                          * x) + ((bondReturns[(session['start']-1928)+i]/100)*y), False]
                except:
                    returns[str(i+1)] = [((marketReturns[-(35-i)]/100)
                                          * x) + ((bondReturns[-(35-i)]/100)*y), False]

        if request.method == "POST":
            if request.form['submitButton'] == 'Flat 5% Rate of Return':
                for i in range(35):
                    returns[str(i+1)] = [0.05, False]
                session['portfolio'] = 'Flat 5% Rate of Return'
            elif request.form['submitButton'] == '100% Equity Returns':
                returnChanger(1, 0)
                session['portfolio'] = '100% Equity Returns'
            elif request.form['submitButton'] == '100% Bond Returns':
                returnChanger(0, 1)
                session['portfolio'] = '100% Bond Returns'
            elif request.form['submitButton'] == '90% Equity, 10% Bonds':
                returnChanger(0.9, 0.1)
                session['portfolio'] = '90% Equity, 10% Bonds'
            elif request.form['submitButton'] == '80% Equity, 20% Bonds':
                returnChanger(0.8, 0.2)
                session['portfolio'] = '80% Equity, 20% Bonds'
            elif request.form['submitButton'] == '70% Equity, 30% Bonds':
                returnChanger(0.7, 0.3)
                session['portfolio'] = '70% Equity, 30% Bonds'
            elif request.form['submitButton'] == '60% Equity, 40% Bonds':
                returnChanger(0.6, 0.4)
                session['portfolio'] = '60% Equity, 40% Bonds'
            elif request.form['submitButton'] == '50% Equity, 50% Bonds':
                returnChanger(0.5, 0.5)
                session['portfolio'] = '50% Equity, 50% Bonds'
            elif request.form['submitButton'] == '40% Equity, 60% Bonds':
                returnChanger(0.4, 0.6)
                session['portfolio'] = '40% Equity, 60% Bonds'
            elif request.form['submitButton'] == '30% Equity, 70% Bonds':
                returnChanger(0.3, 0.7)
                session['portfolio'] = '20% Equity, 80% Bonds'
            elif request.form['submitButton'] == '20% Equity, 80% Bonds':
                returnChanger(0.2, 0.8)
                session['portfolio'] = '20% Equity, 80% Bonds'
            elif request.form['submitButton'] == '10% Equity, 90% Bonds':
                returnChanger(0.1, 0.9)
                session['portfolio'] = '10% Equity, 90% Bonds'

            if request.form['submitButton'] == 'Calculate' and 'year' in request.form:
                if request.form['year'] != '' and request.form['return'] != '':
                    if '0.' in request.form['return']:
                        returns[request.form['year']] = [float(
                            request.form['return']), True]
                    else:
                        try:
                            returns[request.form['year']] = [float(
                                request.form['return'])/100, True]
                        except:
                            pass
            elif request.form['submitButton'] == 'Calculate' and 'Starting Salary' in request.form:
                if request.form['Starting Salary'] != '':
                    try:
                        session['salary'] = float(
                            request.form['Starting Salary'].replace(",", ""))
                    except:
                        pass
                if request.form['Annual Raise'] != '':
                    if '0.' in request.form['Annual Raise']:
                        session['raise'] = float(request.form['Annual Raise'])
                    else:
                        try:
                            session['raise'] = float(
                                request.form['Annual Raise'])/100
                        except:
                            pass
                if request.form['Saving Rate'] != '':
                    if '0.' in request.form['Saving Rate']:
                        session['sr'] = float(request.form['Saving Rate'])
                    else:
                        try:
                            session['sr'] = float(
                                request.form['Saving Rate'])/100
                        except:
                            pass
                if request.form['Rate of Return'] != '':
                    if '0.' in request.form['Rate of Return']:
                        session['ror'] = float(request.form['Rate of Return'])
                    else:
                        try:
                            session['ror'] = float(
                                request.form['Rate of Return'])/100
                        except:
                            pass
                if request.form['Starting Age'] != '':
                    try:
                        session['age'] = int(request.form['Starting Age'])
                    except:
                        pass
                if request.form['Rate of Withdrawal'] != '':
                    if '0.' in request.form['Rate of Withdrawal']:
                        session['row'] = float(
                            request.form['Rate of Withdrawal'])
                    else:
                        try:
                            session['row'] = float(
                                request.form['Rate of Withdrawal'])/100
                        except:
                            pass

        def totaler(total, empCont):
            try:
                for i in range(66 - session['age']):
                    total = (total+((session['salary'] * ((1+session['raise'])**i))*(
                        session['sr']+empCont)))*(1+session['ror'])
                return(total)
            except:
                return(0)

        def valueCreator(vals, total):
            try:
                for i in range(35):
                    vals.append(total*session['row'])
                    total = (total-vals[-1])*(1+float(returns[str(i+1)][0]))
                return vals
            except:
                return([0 for i in range(35)])

        def avgContribution(session, scenarios):
            def helper(session, n, sequence):
                total = 0
                try:
                    for i in range(66-session['age']):
                        total = (
                            total + ((session['salary']*((1+session['raise'])**i))*(session['sr']+n)))*(1+session['ror'])
                except:
                    pass

                vals = []
                try:
                    for i in range(35):
                        vals.append(total*session['row'])
                        total = (total-vals[-1])*(1+(float(sequence[i])/100))
                except:
                    vals = [0 for i in range(35)]

                if (sum(vals)/len(vals)) < pension[0]:
                    return(helper(session, n+0.01, sequence))

                return(n)

            employerContribution = []
            for i in range(len(scenarios)):
                employerContribution.append(
                    helper(session, 0.01, scenarios[i]))

            mean = int((sum(employerContribution) /
                       len(employerContribution))*100)

            return([mean, int(sqrt((sum([(val-(mean/100))**2 for val in employerContribution]))/len(employerContribution))*1000)/1000])

        session['total'] = 0
        session['total'] = totaler(session['total'], 0)

        regVals = []
        retTotal = session['total']
        regVals = valueCreator(regVals, retTotal)

        try:
            pension = [((((session['salary']*((session['raise']+1)**(65-session['age'])))+(session['salary']*((session['raise']+1) **
                        (64-session['age'])))+(session['salary']*((session['raise']+1)**(63-session['age']))))/3)*0.02)*35 for i in range(35)]
        except:
            pension = [0 for i in range(35)]

        marketAvgCont, marketStdDev = avgContribution(
            session, returnCombinations['market'])
        marketTotal = 0
        marketTotal = totaler(marketTotal, marketAvgCont/100)
        marketVals = []
        marketVals = valueCreator(marketVals, marketTotal)

        bondAvgCont, bondStdDev = avgContribution(
            session, returnCombinations['bonds'])
        bondTotal = 0
        bondTotal = totaler(bondTotal, bondAvgCont/100)
        bondVals = []
        bondVals = valueCreator(bondVals, bondTotal)

        M90B10cont, M90B10stdDev = avgContribution(
            session, returnCombinations['90M10B'])
        M90B10total = 0
        M90B10total = totaler(M90B10total, M90B10cont/100)
        M90B10vals = []
        M90B10vals = valueCreator(M90B10vals, M90B10total)

        M80B20cont, M80B20stdDev = avgContribution(
            session, returnCombinations['80M20B'])
        M80B20total = 0
        M80B20total = totaler(M80B20total, M80B20cont/100)
        M80B20vals = []
        M80B20vals = valueCreator(M80B20vals, M80B20total)

        M70B30cont, M70B30stdDev = avgContribution(
            session, returnCombinations['70M30B'])
        M70B30total = 0
        M70B30total = totaler(M70B30total, M70B30cont/100)
        M70B30vals = []
        M70B30vals = valueCreator(M70B30vals, M70B30total)

        M60B40cont, M60B40stdDev = avgContribution(
            session, returnCombinations['60M40B'])
        M60B40total = 0
        M60B40total = totaler(M60B40total, M60B40cont/100)
        M60B40vals = []
        M60B40vals = valueCreator(M60B40vals, M60B40total)

        M50B50cont, M50B50stdDev = avgContribution(
            session, returnCombinations['50M50B'])
        M50B50total = 0
        M50B50total = totaler(M50B50total, M50B50cont/100)
        M50B50vals = []
        M50B50vals = valueCreator(M50B50vals, M50B50total)

        M40B60cont, M40B60stdDev = avgContribution(
            session, returnCombinations['40M60B'])
        M40B60total = 0
        M40B60total = totaler(M40B60total, M40B60cont/100)
        M40B60vals = []
        M40B60vals = valueCreator(M40B60vals, M40B60total)

        M30B70cont, M30B70stdDev = avgContribution(
            session, returnCombinations['30M70B'])
        M30B70total = 0
        M30B70total = totaler(M30B70total, M30B70cont/100)
        M30B70vals = []
        M30B70vals = valueCreator(M30B70vals, M30B70total)

        M20B80cont, M20B80stdDev = avgContribution(
            session, returnCombinations['20M80B'])
        M20B80total = 0
        M20B80total = totaler(M20B80total, M20B80cont/100)
        M20B80vals = []
        M20B80vals = valueCreator(M20B80vals, M20B80total)

        M10B90cont, M10B90stdDev = avgContribution(
            session, returnCombinations['10M90B'])
        M10B90total = 0
        M10B90total = totaler(M10B90total, M10B90cont/100)
        M10B90vals = []
        M10B90vals = valueCreator(M10B90vals, M10B90total)

        contributionList = [marketAvgCont, bondAvgCont, M90B10cont, M80B20cont, M70B30cont,
                            M60B40cont, M50B50cont, M40B60cont, M30B70cont, M20B80cont, M10B90cont]
        contributionCorrespondence = {str(marketAvgCont): ('100% Equity', marketStdDev), str(bondAvgCont): ('100% Bonds', bondStdDev), str(M90B10cont): ('90% Equity 10% Bonds', M90B10stdDev), str(M80B20cont): ('80% Equity 20% Bonds', M80B20stdDev), str(M70B30cont): ('70% Equity 30% Bonds', M70B30stdDev), str(M60B40cont): (
            '60% Equity 40% Bonds', M60B40stdDev), str(M50B50cont): ('50% Equity 50% Bonds', M50B50stdDev), str(M40B60cont): ('40% Equity 60% Bonds', M40B60stdDev), str(M30B70cont): ('30% Equity 70% Bonds', M30B70stdDev), str(M20B80cont): ('20% Equity 80% Bonds', M20B80stdDev), str(M10B90cont): ('10% Equity 90% Bonds', M10B90stdDev)}

        magicNum = (int((sum(contributionList)/11)*100))/100
        magicTotal = 0
        magicTotal = totaler(magicTotal, magicNum/100)
        magicVals = []
        magicVals = valueCreator(magicVals, magicTotal)

        minCont = min(contributionList)
        minPortfolio, minStdDev = contributionCorrespondence[str(minCont)]
        minTotal = 0
        minTotal = totaler(minTotal, minCont/100)
        minVals = []
        minVals = valueCreator(minVals, minTotal)

        maxCont = max(contributionList)
        maxPortfolio, maxStdDev = contributionCorrespondence[str(maxCont)]
        maxTotal = 0
        maxTotal = totaler(maxTotal, maxCont/100)
        maxVals = []
        maxVals = valueCreator(maxVals, maxTotal)

        try:
            salary = "{:,}".format((int(session['salary']*100))/100)
        except:
            salary = 0
        try:
            payRaise = session['raise']*100
        except:
            payRaise = 0
        try:
            sr = session['sr']*100
        except:
            sr = 0
        try:
            ror = session['ror']*100
        except:
            ror = 0
        try:
            age = session['age']
        except:
            age = 0
        try:
            row = session['row']*100
        except:
            row = 0
        try:
            start = str(session['start'])
        except:
            start = '1987'
        try:
            window = session['window']
        except:
            window = '1987-2021'

        portfolio = ''
        try:
            portfolio = session['portfolio']
        except:
            portfolio = 'Flat 5% Rate of Return'

        changedReturns = ''
        for key in returns:
            if returns[key][1] == True:
                if len(changedReturns) == 0:
                    changedReturns = changedReturns + 'Year ' + key + \
                        ': ' + str(int(returns[key][0]*100)) + '%'
                else:
                    changedReturns = changedReturns + ', Year ' + \
                        key + ': ' + str(int(returns[key][0]*100)) + '%'

        return render_template('data.html', form_data=session, regVals=regVals, pension=pension, minVals=minVals, minCont=minCont, minPortfolio=minPortfolio, minStdDev=minStdDev, maxVals=maxVals, maxCont=maxCont, maxPortfolio=maxPortfolio, maxStdDev=maxStdDev, magicVals=magicVals, magicNum=magicNum, portfolio=portfolio, salary=salary, payRaise=payRaise, sr=sr, ror=ror, age=age, row=row, changedReturns=changedReturns, start=start, window=window)
    else:
        return render_template('reRoute.html')


@app.route('/about')
def about():
    if session['loggedIn'] == True:
        return render_template('about.html')
    else:
        return render_template('reRoute.html')