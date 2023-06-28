import subprocess
from config import rclone_bin, location_list, ip_nas
from functions import gen_crypt

rclone_web_acess_options = "serve http --addr :8080"

def web_files_access(index, snapshot):
    value = location_list[index]
    destino = value["destin"]
    list_command = [
        rclone_bin,
        rclone_web_acess_options,
        gen_crypt(f"{destino}.zfs/snapshot/{snapshot}/"),
    ]
    print(f"Acesse o link: http://{ip_nas}:8080")
    print("-" * 30)
    cmd = " ".join(list_command)
    print(cmd)
    subprocess.call(cmd, shell=True)

def get_file():
    for index, value in enumerate(location_list):
        print(index, "-", value["nome"].upper())
    print("-" * 30)
    index_pa = int(input(f"Selecione o PA: "))
    destino = location_list[index_pa]["destin"]
    list_snapshots = (
        subprocess.check_output(f"ls {destino}.zfs/snapshot/", shell=True)
        .decode()
        .split("\n")
    )
    list_snapshots = [i for i in list_snapshots[::-1] if i != '']

    for index, value in enumerate(list_snapshots):
        print(index, "-", value)
    print("-" * 30)
    index_snapshot = int(input(f"Selecione o Snaphost: "))
    snapshot = list_snapshots[index_snapshot]

    web_files_access(index_pa, snapshot)

def get_log():
    log_dir = "/var/log/"
    print(f"Acesse o link: http://{ip_nas}:8080")
    print("-" * 30)
    subprocess.call(f'rclone serve http --addr :8080 {log_dir} --include "backup*" ', shell=True)

repeat_loop = True
while repeat_loop:
    repeat_loop = False
    escolha_funcao = input('Deseja recuperar arquivos ou ver os logs? (R,L): ')

    if escolha_funcao.upper() == 'R':
        get_file()
    elif escolha_funcao.upper() == 'L':
        get_log()
    else:
        print('Escolha invalida! Digite L ou R')
        repeat_loop = True
