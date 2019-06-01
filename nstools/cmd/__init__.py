import six
import subprocess

def shell(command):
    return subprocess.call(command, shell=True)

def shell_out(command):
    try:
        s = subprocess.check_output(command, shell=True)
        if isinstance(s, str):
            return s
        return s.decode()
    except subprocess.CalledProcessError as e:
        print(e)
        return ''
    except Exception as e:
        raise
