#!/usr/bin/python
# coding=utf-8


import requests
import queue
from bs4 import BeautifulSoup
from threading import Thread
import time
import sys


data = queue.Queue()
origUrls = queue.Queue()

'''No need to pass as they are global anyway 
but imho it makes things more obvious'''

    
def getSrc(origUrls):
    

    while not origUrls.empty():
                
        url = origUrls.get(block=False)[0].strip()
        
        try:
            r=requests.get(url)
            data.put({'html':r.text, 'url':url})
        
        #Assuming put() is not likely to surprise us at this point
        #stderr used hereinafter as we want the output to remain 'clean'
        
        except requests.exceptions.RequestException as e:
            print (e, file=sys.stderr)
        

def parse(data):
    
    #just to make sure there's something there by the time we start
     
    time.sleep(2)

    while not data.empty():
        
        try:
                        
            specificData = data.get(block=False)
            soup = BeautifulSoup(specificData['html'],  'html.parser')
            print('####'+specificData['url']+'####')
            links = soup.select('a')
                                
            for link in links:
                
                if link is not None:
                
                    print(link.get('href')+'\n')
        
        #Could be more specific but works for demonstration purposes
        except BaseException as e:
            print('Something went south while trying to get & parse data: {}'.format(e),  file=sys.stderr)
           

def getOrig(path='urlList'):
    
    '''we could also take the path from cl. True, one should add clarifying help text & further 
    tests to evaluate the path and other possible params passed via the cl'''
    
    if len (sys.argv)>1:
        path=sys.argv[1]
    
    try:
        with open (path, 'r') as file:
                for line in file:
                    '''it would be nice to test if a url is indeed a url *before* 
                    trying to connect (possibly in vain) but it seems there's no easy way (enough imports already) & regex is a compromise anyway
                    Here's something (just to make a point) that should get the most obvious fails out of the way'''''
                    if urlTest(line):
                        origUrls.put([line])
                    
    except FileNotFoundError:
                
        print("Something's off with the source file, check that 'urlList' exists \
        in pwd or that you provided a correct path via cl",  file=sys.stderr)
        #no point in going further
        raise (FileNotFoundError)
        
def urlTest(url):
    if '.' not in url or ' ' in url:
        return False
    return True


if __name__ == '__main__':
    #extract *original* urls from file
    getOrig()
    ############################

    
    Thread(target = getSrc,  args=(origUrls, )).start()
    Thread(target = parse,  args=(data, )).start()
