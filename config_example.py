from functions import gen_sftp, gen_smb, gen_crypt_file_name_off

# Max Simlutaneos Threads
maxthreads = 5

# rclone Binary
rclone_bin = "/usr/local/bin/rclone"

# rclone options
rclone_options = "sync -v --ignore-errors"

#Generate obfuscate password
#rclone obscure passwd


location_list = [
    {
        "nome": "example",
        "origin": gen_sftp('ip', 'port', 'user', 'remote_path', 'passwd_obfusqued'),
        "destin": gen_crypt_file_name_off('local_path', 'passwd_obfusqued'),
    },
]