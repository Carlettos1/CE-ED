import subprocess
import re

defaultTime: str = "01:00:00"

helpMessage: str = ""

# types: list | str | None
def getNodes(arg=None) -> str:
    sinfo = ["sinfo", "-O", "Nodes"]
    if type(arg) is str:
        sinfo.append(arg)
    elif type(arg) is list:
        for a in arg:
            sinfo.append(a)
    return getOutput(sinfo).replace("\n", "").replace("NODES", "").replace(" ", "")

def getLength(com: list) -> int:
    return len(getOutput(com).split("\n")) - 2

def getOutput(com: list) -> str:
    return subprocess.check_output(com).decode("utf-8")

def decodeTime(time: str) -> str:
    numero: re.Pattern = re.compile("[1-9]+")
    days: re.Pattern = re.compile("[1-9][dD]")
    hours: re.Pattern = re.compile("[1-9][0-9]{0,3}[hH]")
    minutes: re.Pattern = re.compile("[1-9][0-9]{0,5}[mM]")
    complete: re.Pattern = re.compile("([0-9]{1,2}:){2}[0-9]{2}")

    if re.match(days, time) != None:
        d = int(re.findall(numero, time)[0])
        return str(d*24)+":00:00"
    elif re.match(hours, time) != None:
        return str(h) + ":00:00"
    elif re.match(minutes, time) != None:
        m = int(re.findall(numero, time)[0])
        h = m//60
        m = m%60
        h_str = str(h)
        m_str = str(m)
        m_str = m_str if len(m_str) == 2 else "0" + m_str 
        return h_str + ":" + m_str + ":00"
    elif re.match(complete, time) != None:
        return time
    return defaultTime

def extractParams(i: int, varargs: list) -> str:
    com = ""
    n = i + 1
    while n < len(varargs):
        if varargs[n][0] == "-":
            break
        com += " " + varargs[n]
        n += 1
    return com[1:]

def beautify(original: str) -> str:
    return "\n> " + original.replace("\n", "\n> ")[:-2]

def toCode(original: str, language: str="") -> str:
    return f"```{language}\n{original}```\n"