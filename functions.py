
def gen_sftp(host, port, user, diretorio, sftp_pass):
    param_list = []
    param_list.append(f'--sftp-host {host}')
    param_list.append(f'--sftp-port {port}')
    param_list.append(f'--sftp-user {user}')
    param_list.append(f'--sftp-pass "{sftp_pass}"')
    param_list.append(f'--sftp-shell-type "unix"')
    param_list.append(f'--sftp-md5sum-command "md5 -r"')
    param_list.append(f'--sftp-sha1sum-command "sha1 -r"')
    param_list.append(f'":sftp:{diretorio}"')

    cmd = " ".join(param_list)
    return cmd

def gen_smb(host, user, smb_pass, share):
    param_list = []
    param_list.append(f'--smb-host {host}')
    param_list.append(f'--smb-user {user}')
    param_list.append(f'--smb-pass "{smb_pass}"')
    param_list.append(f'":smb:/{share}"')

    cmd = " ".join(param_list)
    return cmd

def gen_crypt(diretorio, crypto_pass):
    param_list = []
    param_list.append(f'--crypt-remote {diretorio}')
    param_list.append(f'--crypt-filename-encryption "obfuscate"')
    param_list.append(f'--crypt-password "{crypto_pass}"')
    param_list.append(f':crypt:/')

    cmd = " ".join(param_list)
    return cmd

def gen_crypt_encoding(diretorio, crypto_pass):
    param_list = []
    param_list.append(f'--crypt-remote {diretorio}')
    param_list.append(f'--crypt-filename-encoding')
    param_list.append(f'--crypt-password "{crypto_pass}"')
    param_list.append(f':crypt:/')

    cmd = " ".join(param_list)
    return cmd
