import os, sys, string, time
from subprocess import Popen
import dateutil.parser
import configparser
from croniter import croniter
from datetime import datetime
import subprocess

def logMessage(message):
    f = open('./logs/scriptLauncher.log', 'a')
    f.write(str(datetime.now()) + " " + message + "\n")
    f.close()
    print(str(datetime.now()) + " " + message)
    
def doexec(cmd, cwd, confName):
    outfile = open('./logs/' + confName + '.log', 'a')
    outfile.write("-------------------------------------------\n")
    outfile.write("- Starting at " + str(datetime.now()) + "  -\n")
    outfile.write("-------------------------------------------\n")
    if cmd.lower().endswith(".bat"):        
        p = Popen(["cmd", "/c", cmd], cwd=cwd, stdout=outfile, stderr=outfile)
    elif cmd.lower().endswith(".py"):
        p = Popen(["python", cmd], cwd=cwd, stdout=outfile, stderr=outfile)
    elif cmd.lower().endswith(".sh"):
        p = Popen(["sh", cmd], cwd=cwd, stdout=outfile, stderr=outfile)
    else:
        p = Popen(cmd, cwd=cwd, stdout=outfile, stderr=outfile)

def runOnce():
    global numloop
    numloop+=1
    config = configparser.RawConfigParser()
    config.read("conf.cfg")
    for section in config.sections():
        cmd = config.get(section, 'cmd')
        cwd = config.get(section, 'cwd')
        cron = config.get(section, 'cron')
        if cron == 'once':
            if numloop==1:
                doexec(cmd, cwd, section)            
            continue
        if config.has_option(section, 'lastLaunch'):
            lastLaunch = dateutil.parser.parse(config.get(section, 'lastLaunch'))
        else:
            lastLaunch = datetime(2000,1,1)
        iter = croniter(cron, lastLaunch)
        nextLaunch = iter.get_next(datetime)
        if datetime.now() > nextLaunch:     
            config.set(section, 'lastLaunch', datetime.now().isoformat())            
            with open('conf.cfg', 'w') as configfile:
                config.write(configfile)
            logMessage("Launching task " + section)
            doexec(cmd, cwd, section)
            logMessage("Task " + section + " complete")

if not os.path.exists("./logs"):
    os.makedirs("./logs")
numloop=0
logMessage("Starting up scriptLauncher")
while True:    
    runOnce()
    time.sleep(1)