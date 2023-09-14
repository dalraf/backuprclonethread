import os
import zipfile

def rotate_and_zip_logs(log_filename, max_logs):
    # Verifique se o arquivo de log original existe
    if not os.path.exists(log_filename):
        print(f"O arquivo de log '{log_filename}' não existe.")
        return
    
    # Renomeie os arquivos de log existentes, mantendo até o número máximo
    for i in range(max_logs, 0, -1):
        current_log = f"{log_filename}.{i}"
        next_log = f"{log_filename}.{i+1}" if i < max_logs else f"{log_filename}.1"
        if os.path.exists(current_log):
            os.rename(current_log, next_log)
    
    # Renomeie o arquivo de log original para .1
    os.rename(log_filename, f"{log_filename}.1")
    
    # Crie um novo arquivo de log vazio
    open(log_filename, 'w').close()
    
    # Comprima os arquivos de log antigos em um arquivo zip
    log_zipfile = f"{log_filename}_logs.zip"
    with zipfile.ZipFile(log_zipfile, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i in range(1, max_logs + 1):
            log_to_zip = f"{log_filename}.{i}"
            if os.path.exists(log_to_zip):
                zipf.write(log_to_zip, os.path.basename(log_to_zip))
                os.remove(log_to_zip)
    
    print(f"Rotação e compressão concluídas. Arquivos antigos foram movidos para '{log_zipfile}'.")

# Exemplo de uso:
log_filename = "mylog.log"
max_logs = 5
rotate_and_zip_logs(log_filename, max_logs)
