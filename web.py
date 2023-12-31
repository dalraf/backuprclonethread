from flask import Flask, render_template, request, jsonify, redirect
import subprocess
import re
from functions import *
from config import rclone_bin, location_list, ip_nas

app = Flask(__name__)

rclone_web_acess_options = "serve http --addr :8080"

@app.route("/")
def index():
    subprocess.run("killall rclone", shell=True, check=False)
    location_list_index = list(enumerate(location_list))
    return render_template("index.html", location_list_index=location_list_index)


@app.route("/web-files-access", methods=["POST", "GET"])
def web_files_access():
    if request.method == "GET":
        return redirect("/")
    else:
        if request.form["index_pa"] == "" or request.form["snapshot"] == "":
            return redirect("/")
        else:
            index_pa = int(request.form["index_pa"])
            snapshot = request.form["snapshot"]
            value = location_list[index_pa]
            destino = value["destin"].localpath
            recover_function = value["destin"].cmd_recover
            if destino[-1] == "/":
                destino = destino[:-1]
            list_command = [
                rclone_bin,
                rclone_web_acess_options,
                recover_function(f"{destino}/.zfs/snapshot/{snapshot}/"),
            ]
            cmd = " ".join(list_command)
            rclone_process_pid = subprocess.Popen(cmd, shell=True).pid
            return render_template(
                "index.html",
                message=(
                    f"Permissão concedida para acessar o diretório.<br>"
                    f"Acesse <a href='http://{ip_nas}:8080' target='_blank'>aqui</a> para explorar.<br>"
                    f"O processo está em execução com o PID {rclone_process_pid}."
                    f"<br><br><a href='/'>Reniciar app</a>"
                ),
            )


@app.route("/get-snapshots/<int:index_pa>")
def get_snapshots(index_pa):
    value = location_list[index_pa]
    destino = value["destin"].localpath
    if destino[-1] == "/":
        destino = destino[:-1]
    list_snapshots = (
        subprocess.check_output(f"ls {destino}/.zfs/snapshot/", shell=True)
        .decode()
        .split("\n")
    )
    list_snapshots = [i for i in list_snapshots[::-1] if i != ""]

    return jsonify({"snapshots": list_snapshots})


@app.route("/get-log")
def get_log():
    log_dir = "/var/log/"
    subprocess.call(
        f'rclone serve http --addr :8080 {log_dir} --include "backup*" ', shell=True
    )

    return render_template("index.html", message="Acesso aos logs concedido.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
