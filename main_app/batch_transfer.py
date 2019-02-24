"""
Klasa za ftp komunikaciju. Upotrebi https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
"""
import ftplib


class BatchTransfer:
    HOST_ADRESS = '41.231.5.77'
    USER = 'Serb1'
    PASSWORD = 'Serb1'

    def __init__(self):
        try:
            self.ftp = ftplib.FTP(BatchTransfer.HOST_ADRESS)
            self.ftp.login(user=BatchTransfer.USER, passwd=BatchTransfer.PASSWORD)
        except ftplib.all_errors as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


    def change_directory(self, dir):
        self.ftp.cwd(dir)


    def get_folder(self, folder):
        pass
