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
    os.system('. ../install.sh && clear')
    os.system('clear')
    print('start again!')
    exit(0)

class screener:

    # load configuration
    with open('../config.yml') as f:
        payload = yaml.safe_load(f)
    
    # load database
    with open('./dump.json') as f:
        dumpReadIn = json.load(f)

    # define global parameters
    CONF = payload
    DATE = date.today()
    API = discogs_client.Client('ExampleApplication/0.1', user_token=CONF['credentials']['key'])  # login to discogs
    LOG = logger(f'../logs/logging_{DATE.strftime("%d-%m-%Y")}.log')
    DB = dumpReadIn # database remembers offers belonging to an id on discogs
    VINYLS = CONF['vinyls']

    LOG.note('Welcome to discogsScreener! See the project https://github.com/B0-B/discogsScreener if you want to contribute!', save=False, logType='Bot', logTypeCol='\033[94m')

    def dump(self):
        with open('./dump.json', 'w+') as f:
            json.dump(self.DB, f)
    
    def screen(self):
        self.LOG.note('Screening the market ...', save=False, logType='Bot', logTypeCol='\033[94m', wait=1)
    
    def run(self):

        '''
        Main loop method for the screener.
        This is meant to be executed as 
            s = screener()
            s.run()
        '''

        try:
            # show what is tracked
            searchList = ''
            for v in self.VINYLS.values():
                if v['artist'] + v['album'] == '':
                    searchList += f"\n [{v['cat']}]"
                else:
                    searchList += f"\n [{v['cat']}] {v['artist']} - {v['album']} ({v['year']})"
            self.LOG.note(f'Screening for:{searchList}', logType='Bot', logTypeCol='\033[94m')

            # check if the searchList is known in DB
            dbKeys = self.DB.keys()
            for v in self.VINYLS.values():
                if v['cat'] not in dbKeys:
                    self.DB[v['cat']] = []

            # start the service loop
            while(True):
                self.screen()

        except KeyboardInterrupt:
            self.LOG.note('Terminating service.', logType='Bot', logTypeCol='\033[94m')
            
        except Exception as e:
            self.LOG.note('something went wrong ...', logType='error')
        
        finally:
            # dump the tracking offers
            self.dump()

        # leave python
        exit(0)

        
if __name__ == '__main__':
    # start service
    s = screener()
    s.run()
