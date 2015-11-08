import telnetlib
import time

class PromptError(Exception):
    pass

def TELNETlogin(loginfields):
    tel = telnetlib.Telnet()
    hostname = loginfields[1]
    username = loginfields[2]
    password = loginfields[3]
    configlist = ["enable","show ip inter br"]
    expectwords = ["sername:\s*$","ogin:\s*$","assword:\s*$",">\s*$","#\s*$"]
    try:
        tel.open(hostname)
        stdout = tel.expect(expectwords,timeout=10)
        if stdout[0] == -1:
            raise PromptError("There are not any Prompts match")
        tel.write(username+"\r\n")
        stdout = tel.expect(expectwords,timeout=10)
        if stdout[0] == -1:
            raise PromptError("There are not any Prompts match")
        tel.write(password+"\r\n")
        stdout = tel.expect(expectwords,timeout=10)
        if stdout[0] == -1:
            raise PromptError("There are not any Prompts match")
    except PromptError,e:
        print e.message
    except Exception,e:
        print e.message
    else:
        config = {}
        while configlist:
            tel.write(configlist[0]+"\r\n")
            if configlist[0].startswith("en"):
                try:
                    stdout = tel.expect(expectwords,timeout=10)
                    print stdout
                    if stdout[0] == -1:
                        raise PromptError("There are not any Prompts match")
                except PromptError,e:
                    print e.message
                except Exception,e:
                    print e.message
                else:
                    print "enable"
                    tel.write("test"+"\r\n")
                    tel.expect(expectwords,timeout=10)
                    configlist.pop(0)
            else:
                time.sleep(5)
                config[configlist[0]] = tel.read_very_eager()
                configlist.pop(0)
        return config
    finally:
        tel.close()


if __name__ == "__main__":
    fields = ["telnet","192.168.3.202","test","test"]
    rr = TELNETlogin(fields)
    print rr
