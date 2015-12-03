# -*- coding: utf8 -*-

import paramiko
import telnetlib
import os,sys,re,time,csv
#import multiprocessing as mul
import logging
reload(sys)
sys.setdefaultencoding("utf8")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s Funcname:(%(funcName)s) [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=os.path.join(sys.path[0],'log.txt'),
                    filemode='a')

class PromptError(Exception):
    pass

def Login(fieldlist):
    result = None
    status = None
    logingtype = fieldlist[0]
    # print logingtype
    if logingtype == "ssh":
        status,result = SSHlogin(fieldlist[1:])
    elif logingtype == "telnet":
        status,result = TELNETlogin(fieldlist[1:])
    return status,result

def SSHlogin(loginfields):
    # print loginfields
    hostname = loginfields[1]
    username = loginfields[2]
    password = loginfields[3]
    userpawd = loginfields[4] if loginfields[4] else None
    configlist = loginfields[5]
    usermode = ['enable','system-view']
    client = paramiko.SSHClient()
    known_hosts_file = os.path.join(sys.path[0],"known_hosts")
    if not os.path.exists(known_hosts_file):
        with file(known_hosts_file,"w") as f:
            pass
    client.load_host_keys("known_hosts")
    #time.sleep(10)
    #hosts= client.get_host_keys()
    #print hosts.items()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname,username=username,password=password,look_for_keys = False,allow_agent = False)
        clientbuf = client.invoke_shell()
        output = clientbuf.recv(1000)      
    except Exception,e:
        logging.error(e.message+"connect error")
        return 0,None
    else:
        config = {}
        while configlist:
            print configlist[0]
            clientbuf.send(configlist[0]+"\n")
            time.sleep(1)
            #print "OK"
            if configlist[0] in usermode :
                if not userpawd == None :
                    clientbuf.send(userpawd+"\n")
                    #print clientbuf.recv(1000)
                    configlist.pop(0)
            else:
                config[configlist[0]]=cont=clientbuf.recv(5000)
                #print cont
                configlist.pop(0)
        return 1,config
    finally:
        client.close()


def TELNETlogin(loginfields):
    tel = telnetlib.Telnet()
    #print loginfields
    hostname = loginfields[1]
    username = loginfields[2]
    password = loginfields[3]
    userpawd = loginfields[4] if loginfields[4] else None
    configlist = loginfields[5]
    expectwords = ["sername:\s*$","ogin:\s*$","assword:\s*$",">\s*$","#\s*$"]
    usermode = ['enable','system-view']
    try:
        tel.open(hostname)
        stdout = tel.expect(expectwords,timeout=10)
        if stdout[0] == -1:
            raise PromptError("Login:There are not any Prompts match")
        tel.write(username+"\r\n")
        stdout = tel.expect(expectwords,timeout=10)
        if stdout[0] == -1:
            raise PromptError("Username:There are not any Prompts match")
        tel.write(password+"\r\n")
        stdout = tel.expect(expectwords,timeout=10)
        if stdout[0] == -1:
            raise PromptError("Password:There are not any Prompts match")
    except PromptError,e:
        logging.error(e.message)
        return 0,None
    except Exception,e:
        logging.error(e.message+"connect error")
        return 0,None
    else:
        config = {}
        while configlist:
            tel.write(configlist[0]+"\r\n")
            print configlist[0]+"-"*10
            time.sleep(1)
            if configlist[0] in usermode :
                try:
                    stdout = tel.expect(expectwords,timeout=10)
                    if stdout[0] == -1:
                        raise PromptError("Usermode:There are not any Prompts match")
                except PromptError,e:
                    logging.error(e.message)
                    return 0,None
                except Exception,e:
                    logging.error(e.message)
                    return 0,None
                else:
                    #提示输入enable密码，如果有的话一定要写上
                    if not userpawd == None :
                        tel.write(userpawd+"\r\n")
                        #print tel.expect(expectwords,timeout=10)
                        configlist.pop(0)
            else:
                config[configlist[0]] = tel.read_very_eager()
                configlist.pop(0)
        logging.debug("%s is ok"%hostname)
        return 1,config
    finally:
        tel.close()
        
def Readconfig(filepath):
    hostinfo = []
    with file(filepath,'r') as f:
        fc = csv.reader(f)
        for linec,cont in enumerate(fc,1):
            if linec == 1:
                continue
            else:
                hostinfo.append(cont[:-1]+[cont[-1].split('\n')])
    return hostinfo

def Writeconfig(filepath, config):
    repl = re.compile("\s+")
    if config is not None:
        for keys in config:
            name = repl.sub("_",keys)+".log"
            with file(os.path.join(filepath,name),'w') as f:
                f.write(config[keys])

def main(faname, outputpath = None):
    configfile = os.path.join(sys.path[0],faname)
    hostinfos = Readconfig(configfile)
    today = time.strftime("%Y-%m-%d")
    if outputpath == None:
        datapath = os.path.join(sys.path[0],today)
    else:
        datapath = os.path.join(outputpath,today)
    if not os.path.exists(datapath):
        os.mkdir(datapath)
    for perhost in hostinfos:
        print perhost
        ipname = perhost[2]
        status,result = Login(perhost)
        # print status
        directname = None
        if status == 0:
            directname = "failure_"+ipname
        elif status == 1:
            directname = ipname
        filepath = os.path.join(datapath,directname)
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        Writeconfig(filepath,result)

"""
    mul.freeze_support()
    system_core = mul.cpu_count()
    while 1:
        print "检测到系统为%s核CPU，请选择小于等于物理核心数量的进程数！"%system_core
        getpro = raw_input("请输入占用的核心数：")
        try:
            inputpro = int(getpro)
        except ValueError:
            pass
        else:
            if inputpro > system_core:
                pass
            else:
                break
    cpool = mul.Pool(inputpro)
    success_count = 0
    result = []
    for line in hosts:
        #print line
        if line[0] == "telnet":
            status,configs = TELNETlogin(line[1:])
        elif line[0] == "ssh":
            status,configs = SSHlogin(line[1:])
    result = [cpool.apply_async(SSHlogin,(hosts,)) for hosts in whole]
    cpool.close()
    cpool.join()
"""

if __name__ == '__main__':
    configfile = "facility.csv"
    output = ""
    main(configfile,None)
