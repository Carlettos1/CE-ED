import re
from util import getLength, getNodes, getOutput, beautify, toCode

## Commands alias
show = ["show"]
status = ["status"]
qos = ["qos"]
jobs = ["jobs", "squeue"]
nodes = ["nodes", "node"]
usuario = ["usuario", "user", "u"]

def sshow():
    ## Up Time
    pattern = re.compile("up ([0-9]+) [a-z]+, ( ?[0-9]{1,2}:[0-9]{2}|[0-9]{1,2} [a-z]{3})")
    days, hours = re.findall(pattern, getOutput("uptime"))[0]
    ## Jobs Running
    running = str(getLength(["squeue", "-t", "RUNNING"]))
    ## Jobs in Q
    pending = str(getLength(["squeue", "-t", "PENDING"]))
    ## Nodes
    allNodes = getNodes()
    responsives = getNodes("-r")
    dead = getNodes("-d")
    allocated = getNodes(["-t", "allocated"])
    down = getNodes(["-t", "down"])
    mixed = getNodes(["-t", "mixed"])
    idle = getNodes(["-t", "idle"])
    ## Connected Users
    users = str(getLength("w"))
    return f"""
Up Time: {days} d {hours}
Jobs Running: {running}
Jobs Pending: {pending}
Total Nodes: {allNodes}
Responsive Nodes: {responsives}
Dead Nodes: {dead}
Idle Nodes: {idle}
Midex Nodes: {mixed}
Allocated Nodes: {allocated}
Down Nodes: {down}
Connected Users: {users}
"""

def sstatus():
    return "bot status"

def sqos():
    return getOutput(["sacctmgr", "show", "qos", "format=name,priority,maxWall"])

def sjobs():
    return getOutput(["squeue", "-l"])

def snodes():
    return getOutput("sinfo")

def susuario():
    return "info user"

def tryTo(command: str):
    if command in show:
        return toCode(sshow(), "scala")
    if command in status:
        return sstatus()
    if command in qos:
        return toCode(sqos(), "hs")
    if command in jobs:
        return toCode(sjobs(), "hs")
    if command in nodes:
        return toCode(snodes(), "hs")
    if command in usuario:
        return susuario()