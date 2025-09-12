import os
from ftplib import FTP
current_directory=os.path.dirname(os.path.abspath(__file__))

directory=f"{current_directory}/siogas/img/join"


# FTP settings
login = "ocefisi_1"
secret = "Oc3f1s1O*"  # FTP password
uploadsite = "172.30.10.5"  # FTP server IP address
uploadfolder = "/newoceano2023/Oceano/siogas_figuras"  # Folder to upload to


file_list=os.listdir(directory)

# FTP upload function
def upload_file(local_file, remote_file):
    try:
        # Connect to the FTP server
        ftp = FTP(uploadsite)
        ftp.login(user=login, passwd=secret)

        # Open the file to be uploaded
        with open(local_file, 'rb') as f:
            # Upload the file to the specified remote path
            ftp.storbinary(f"STOR {remote_file}", f)

        print(f"Successfully uploaded {local_file} to {remote_file}")

        # Close FTP connection
        ftp.quit()
    except Exception as e:
        print(f"Failed to upload {local_file}: {e}")

# Loop through the file list and upload each file
for file_name in file_list:
    local_file_path = os.path.join(directory, file_name)
    remote_file_path = os.path.join(uploadfolder, file_name)
    upload_file(local_file_path, remote_file_path)