import logging
import logging.handlers
import gzip
import os

class CompressingRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self):
        super().doRollover()

        # Após a rotação, comprima o arquivo anterior
        if self.backupCount > 0:
            old_log = self.baseFilename + ".1"
            if os.path.exists(old_log):
                with open(old_log, 'rb') as f_in, gzip.open(old_log + '.gz', 'wb') as f_out:
                    f_out.writelines(f_in)

                os.remove(old_log)