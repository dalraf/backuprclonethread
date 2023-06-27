maxthreads = 5

#Password obfuscate for rclone
sftp_pass = ''
crypto_pass = ''

# rclone Binary
rclone_bin = "/usr/local/bin/rclone"

# rclone options
rclone_options = "sync -v"

# List of locations and destiny

ip_nas = 'IP'

location_list = []
location_list.append(
    {
        "nome": "name",
        "origin": ('IP', 'Port', 'user', 'dir'),
        "destin": ('dir'),
    }
)
