#!/usr/bin/python3

'''
This is the core of the screener.
'''

import sys, os, yaml, json
from datetime import date
sys.path.append('..')

# try to import modules otherwise run the install script
try:
    from prology.log import logger
    import discogs_client
except:
    print('\033[0;31m'+'Dependencies are not installed yet, installing ...'+'\033[0m')
    os.system('. ../install.sh')
    os.system('clear')

class screener:

    # load configuration
    with open('../config.yml') as f:
        payload = yaml.safe_load(f)
        print('config:', payload)
    with open('./dump.json') as f:
        dumpReadIn = json.load(f)

    # define global parameters
    CONF = payload
    DATE = date.today()
    API = discogs_client.Client('ExampleApplication/0.1')
    LOG = logger(f'../logs/logging_{DATE.strftime("%d-%m-%Y")}.log')
    DB = dumpReadIn
    VINYLS = CONF['vinyls']

    # login to discogs
    API.set_consumer_key(CONF['credentials']['key'], CONF['credentials']['secret'])
    LOG.note('Welcome to discogsScreener! See the project https://github.com/B0-B/discogsScreener if you want to contribute!', save=False, logType='Bot', logTypeCol='\033[94m')

    
    def run(self):

        # show what is tracked
        self.LOG.note('Screening for:', logType='Bot', logTypeCol='\033[94m')
        for v in self.VINYLS.values():
            print('v:', v)
            if v.artist + v.album == '':
                print(' '+v.id)
            else:
                print(f' {v.id}: {v.artist} - {v.album} ({v.year})')

if __name__ == '__main__':
    s = screener()
    s.run()
