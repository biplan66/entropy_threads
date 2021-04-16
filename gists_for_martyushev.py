import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import pymongo
import re
import csv

NeedWriteHeader = True


def npPlot(mu = 0, sigma = 1.0):

    s = np.random.normal(mu, sigma, 1000)

    fig, ax = plt.subplots(figsize=(15, 15))
    _, bins, _ = ax.hist(s, 20, density=1, alpha=0.5)
    fig.savefig("export/normal_first_" + str(mu) + '-' + str(sigma) + ".png")
    a = 10

def writeItemToCsv(items: dict):
    global NeedWriteHeader
    with open('export/results.csv', 'a', newline='') as csvfile:
        spamwriter = csv.DictWriter(csvfile, items.keys(), delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if NeedWriteHeader:
            spamwriter.writeheader()
            NeedWriteHeader = False
        spamwriter.writerow(items)

def pythonGauss(mu = 0, sigma = 1.0):
    from random import gauss

    s = [gauss(mu, sigma) for _ in range(1000)]

    fig, ax = plt.subplots(figsize=(15, 15))
    _, bins, _ = ax.hist(s, 20, density=1, alpha=0.5)
    fig.savefig("export/normal_second_" + str(mu) + '-' + str(sigma) + ".png")

def drawDistrs(mu = 0, sigma = 1/5):
    npPlot(mu, sigma)
    pythonGauss(mu, sigma)

def getDistrsFromString(params):
    import json
    distributionPos = params.find("distribution\":")
    if distributionPos >= 0:
        bracket = params.find("}", distributionPos)
        return params[distributionPos + 15:bracket+1]
    return None

if __name__ == '__main__':
    import json
    res1 = re.search("J1\^2 \+ [^\s]*J1\*J2 \+ J2\^2", "J1^2 + J1*J2 + J2^2")
    res2 = re.search("J1\^2 \+ [^\s]*J1\*J2 \+ J2\^2", "J1^2 + 3*J1*J2 + J2^2")
    res3 = re.search("J1\^2 \+ [^\s]*J1\*J2 \+ J2\^2", "J1^2 + 2J1*J2 + J2^2")
    pass
    client = pymongo.MongoClient()
    db = client['threads_modelling']

    cnt = 0
    modelling = []
    f = open("export/temp_file.txt", "w")
    for item in db.results.find():
        if re.search("J1\^2 \+ [^\s]*J1\*J2 \+ J2\^2", item['equation']) != None:
            strinS = json.dumps(item['first'])
            res = db.params.find_one({'_id': item['params']})
            equation = item['equation']
            wins = item['wins']
            coef = wins / int(res['selectionCounInUpperLeague'])

            del res['_id']
            try:
                distrs = json.loads(getDistrsFromString(strinS))
                item = {
                    'equation': equation,
                    'coef': coef,
                    'sigma': distrs['sigma'],
                    'wins': wins,
                    # 'params': res
                }
                item.update(res)
                writeItemToCsv(item)
                # modelling.append(item)
            except:
                pass
            # print(item['_id'], getDistrsFromString(strinS),
            # json.dumps(res))
            cnt += 1

    # modelling = sorted(modelling, key=lambda item: item['coef'], reverse=True)
    # con = sqlite3.connect("export/results.db")
    # con.execute("""
    #     CREATE TABLE IF NOT EXISTS "results" (
    #     "equation"	TEXT,
    #     "wins"	INTEGER,
    #     "coef"	REAL,
    #     "sigma"	REAL,
    #     "leagueSizePerThread"	INTEGER,
    #     "leagueConcatingTimes"	INTEGER,
    #     "leagueLeaderChooseTimes"	INTEGER,
    #     "countOfLeagues"	INTEGER,
    #     "selectionFromLeagueSize"	INTEGER,
    #     "selectionCountInUpperLeague"	INTEGER);
    # """)
    #
    # for item in modelling:
    #     con.execute(f"""INSERT INTO results VALUES ('{item['equation']}', {item['wins']}, {item['coef']}, {item['disr']['sigma']}, {item['params']['leagueSizePerThread']}, {item['params']['leagueConcatingTimes']}, {item['params']['leagueLeaderChooseTimes']}, {item['params']['countOfLeagues']}, {item['params']['selectionFromLeagueSize']}, {item['params']['selectionCounInUpperLeague']});""")
    #     # f.write(f"{item['equation']}, {item['coef']}, {item['disr']}, {item['params']}\n")
    # con.commit()
    # con.close()
    # f.close()

    print("Total counters:", cnt)