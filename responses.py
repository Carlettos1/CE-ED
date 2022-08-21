import random
import subprocess
import re

#Cluster status texts
def queue_status():
    x = subprocess.check_output(['squeue', '-l'])
    return str(x.decode('utf-8'))

def cluster_status():
    x = subprocess.check_output(['sinfo'])
    return str(x.decode('utf-8'))

#User class
class user():
    name = None

    def __init__(self, name):
        self.name = name
    
    def show_jobs(self):
        print(f'valor de self.name = {self.name}')
        x = subprocess.check_output(['squeue', '-l', '-u', self.name])
        return str(x.decode('utf-8'))

    def create_slurm(self, varargs: list) -> str:
        command = open("simple").read()
        NAME = self.name
        NTASKS = "1"
        OUT = "srun"
        ERR = "srun"
        TIME = "01:00:00"
        COMMAND = ""
        MODULES = []
        for i in range(len(varargs)):
            arg = varargs[i]
            if arg == "-t":
                TIME = self.decode_time(varargs[i+1])
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
                COMMAND = self.get_command(i, varargs)
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
        command = command.replace("MODULES", "\nmodule load ".join(MODULES))
        return "> ```bash\n> " + command.replace("\n", "\n> ") + "```\n"
    
    def decode_time(self, time: str) -> str:
        numero: re.Pattern = re.compile("[1-9]+")
        days: re.Pattern = re.compile("[1-9][dD]")
        hours: re.Pattern = re.compile("[1-9][0-9]{0,3}[hH]")
        minutes: re.Pattern = re.compile("[1-9][0-9]{0,5}[mM]")
        complete: re.Pattern = re.compile("([0-9]{1,2}:){2}[0-9]{2}")
        if re.match(days, time) != None:
            d = int(re.findall(numero, time)[0])
            return str(d*24)+":00:00"
        if re.match(hours, time) != None:
            return str(h) + ":00:00"
        if re.match(minutes, time) != None:
            m = int(re.findall(numero, time)[0])
            h = m//60
            m = m%60
            h_str = str(h)
            m_str = str(m)
            m_str = m_str if len(m_str) == 2 else "0" + m_str 
            return h_str + ":" + m_str + ":00"
        if re.match(complete, time) != None:
            return time
        return "01:00:00"

    def get_command(self, i: int, varargs: list) -> str:
        com = ""
        n = i + 1
        while n < len(varargs):
            if varargs[n][0] == "-":
                break
            com += " " + varargs[n]
            n += 1
        return com

def handle_response(message) -> str:
    p_message = message.lower()

    p_message = p_message.strip().split()

    n = len(p_message)

    #if name is given
    name = None
    if p_message[0][0] == "<":
        name = p_message[0][1:-1]

    #show queue status
    if n == 1 and p_message[0] == 'queue':
        msg = queue_status()
        return str(msg)

    #show cluster status
    if n == 1 and p_message[0] == 'status':
        msg = cluster_status()
        return str(msg)

    if n > 1 and name != None:
        command = p_message[1]
        u = user(name)
        if command == 'list':
            msg = u.show_jobs()
            return msg
        if command == "create":
            return u.create_slurm(p_message[2:])
        return f'usuario {name} y comando {command}'

    if p_message[0] == 'hello':
        return 'Hey There!'

    if p_message[0] == 'roll':
        return str(random.randint(1, 6))

    if p_message[0] == "!help":
        return "This is a help message."
    return f'El mensaje {p_message} no prendio cabros'
