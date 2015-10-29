'''

 @Version:   2.7.10 
 @Author:    Tacoff
 @DateTime:  2015-10-28

'''
import datetime

def request_name(func):
    def wrapper(name,sex):
        now = str(datetime.datetime.now())
        if sex == "female":
            print "hello female %s"%now
        else:
            print "hello male %s"%now
        func(name,sex)
    return wrapper


@request_name
def sysout(name,sex):
    print "hello %s"%name


def request_with_argu("")

if __name__ == "__main__":
    sysout("tacoff","male")
