from flask import Flask, render_template, request
import subprocess
import re
from functions import *
from config import rclone_bin, location_list, ip_nas

app = Flask(__name__)

rclone_web_acess_options = "serve http --addr :8080"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/web-files-access", methods=["POST"])
def web_files_access():
    index_pa = int(request.form["index_pa"])
    snapshot = request.form["snapshot"]
    value = location_list[index_pa]
    destino = value["destin"].localpath
    recover_function = value["destin"].cmd_recover
    list_command = [
        rclone_bin,
        rclone_web_acess_options,
        recover_function(f"{destino}.zfs/snapshot/{snapshot}/"),
    ]

    print(f"Acesse o link: http://{ip_nas}:8080")
    print("-" * 30)
    cmd = " ".join(list_command)
    print(cmd)
    subprocess.call(cmd, shell=True)

    return render_template("index.html", message="Acesso ao diretório concedido.")

@app.route("/get-file")
def get_file():
    for index, value in enumerate(location_list):
        print(index, "-", value["nome"].upper())
    print("-" * 30)
    index_pa = int(input(f"Selecione o PA: "))
    destino = location_list[index_pa]["destin"].localpath
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

    return render_template("index.html", message="Acesso ao diretório concedido.")

@app.route("/get-snapshots/<int:index_pa>")
def get_snapshots(index_pa):
    value = location_list[index_pa]
    destino = value["destin"].localpath
    list_snapshots = (
        subprocess.check_output(f"ls {destino}.zfs/snapshot/", shell=True)
        .decode()
        .split("\n")
    )
    list_snapshots = [i for i in list_snapshots[::-1] if i != '']

    return jsonify({"snapshots": list_snapshots})


@app.route("/get-log")
def get_log():
    log_dir = "/var/log/"
    print(f"Acesse o link: http://{ip_nas}:8080")
    print("-" * 30)
    subprocess.call(f'rclone serve http --addr :8080 {log_dir} --include "backup*" ', shell=True)

    return render_template("index.html", message="Acesso aos logs concedido.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
