from config import sftp_pass, crypto_pass

def gen_sftp(host, port, user, diretorio):
    param_list = []
    param_list.append(f'--sftp-host {host}')
    param_list.append(f'--sftp-port {port}')
    param_list.append(f'--sftp-user {user}')
    param_list.append(f'--sftp-pass "{sftp_pass}"')
    param_list.append(f'--sftp-shell-type "unix"')
    param_list.append(f'--sftp-md5sum-command "md5 -r"')
    param_list.append(f'--sftp-sha1sum-command "sha1 -r"')
    param_list.append(f':sftp:{diretorio}')

    cmd = " ".join(param_list)
    return cmd

def gen_crypt(diretorio):
    param_list = []
    param_list.append(f'--crypt-remote {diretorio}')
    param_list.append(f'--crypt-filename-encryption "obfuscate"')
    param_list.append(f'--crypt-password "{crypto_pass}"')
    param_list.append(f':crypt:/')

    cmd = " ".join(param_list)
    return cmd
    
