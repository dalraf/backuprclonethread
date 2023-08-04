import threading
import subprocess
from logging.handlers import RotatingFileHandler
import random
import sys
from config import rclone_bin, rclone_options, location_list
from functions import gen_sftp, gen_crypt


if not len(sys.argv) > 1:
    random.shuffle(location_list)

maxthreads = 3
sema = threading.Semaphore(value=maxthreads)
threads = list()


def task(value):
    sema.acquire()
    nome = value["nome"]
    log_file = f"/var/log/backup{nome}.log"
    rclone_log_command = f"--log-file={log_file}"
    list_command = [
        rclone_bin,
        rclone_options,
        value["origin"],
        value["destin"],
        rclone_log_command,
    ]
    command = " ".join(list_command)
    print(command)
    rotate_log = RotatingFileHandler(log_file, backupCount=20)
    try:
        rotate_log.doRollover()
    except Exception as e:
        print(e.args[0])
    subprocess.call(command, shell=True)
    sema.release()


if len(sys.argv) > 1:
    if sys.argv[1] == "list":
        for index, item in enumerate(location_list):
            print(index, item["nome"])
    else:
        indice = int(sys.argv[1])
        value = location_list[indice]
        task(value)
else:
    for indice, value in enumerate(location_list):
        thread = threading.Thread(target=task, args=(value,))
        threads.append(thread)
        thread.start()
