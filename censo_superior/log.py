def log_printer(msg, log_name='log'):
    print(msg)

    f = open(str(log_name) + ".txt", "a")
    f.write(str(msg) + '\n')
    f.close()
