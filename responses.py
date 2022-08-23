from util import decodeTime, extractParams, beautify, toCode, getOutput, defaultTime, helpMessage
from system_commands import tryTo

_list = ["list", "jobs", "squeue"]
create = ["create"]

#User class
class user():
    name = None

    def __init__(self, name):
        self.name = name
    
    def show_jobs(self):
        return getOutput(["squeue", "-l", "-u", self.name])

    def create_slurm(self, varargs: list) -> str:
        command = open("simple").read()
        NAME = self.name
        NTASKS = "1"
        OUT = "srun"
        ERR = "srun"
        TIME = defaultTime
        COMMAND = ""
        MODULES = []
        for i in range(len(varargs)):
            arg = varargs[i]
            if arg == "-t":
                TIME = decodeTime(varargs[i+1])
                pass
            elif arg == "-log":
                OUT = varargs[i+1]
                ERR = varargs[i+1]
                pass
            elif arg == "-n":
                NTASKS = varargs[i+1]
                pass
            elif arg == "--name":
                NAME = varargs[i+1]
                pass
            elif arg == "-c":
                COMMAND = extractParams(i, varargs)
                pass
            elif arg == "-modules" or arg == "-mod" or arg == "-m":
                n = i + 1
                while n < len(varargs):
                    MODULES.append(varargs[n])
                    n += 1
                break
            pass
        command = command.replace("NAME", NAME)
        command = command.replace("NTASKS", NTASKS)
        command = command.replace("OUT", OUT)
        command = command.replace("ERR", ERR)
        command = command.replace("TIME", TIME)
        command = command.replace("command", COMMAND)
        command = command.replace("MODULES", "\nmodule load ".join([""] + MODULES))
        return beautify(toCode(command, "bash"))

def handle_response(content: str) -> str:
    message = content.lower().strip().split(" ")
    n = len(message)
    if n < 2:
        if n == 1 and message[0] == "help":
            return beautify(helpMessage)
    
    if message[0] == "system":
        return tryTo(message[1])
    else:
        u = user(message[0])
        command = message[1]
        if command in _list:
            return toCode(u.show_jobs(), "hs")
        if command in create:
            return u.create_slurm(message[2:])
