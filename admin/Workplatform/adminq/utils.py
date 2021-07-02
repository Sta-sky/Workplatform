import psutil


def get_os_info():
    # 循环磁盘分区
    partition = psutil.disk_usage('/')
    percentage = partition.percent
    read = psutil.disk_io_counters().read_bytes // 1024 // 1024
    r_time = psutil.disk_io_counters().read_time // 1000
    write = psutil.disk_io_counters().write_bytes // 1024 // 1024
    w_time = psutil.disk_io_counters().write_time / 1000
    virtual_memory = psutil.virtual_memory()
    used_memory = round(virtual_memory.used / 1024 / 1024 / 1024, 2)
    free_memory = round(virtual_memory.total / 1024 / 1024 / 1024, 2) - used_memory
    memory_percent = used_memory / round(virtual_memory.total / 1024 / 1024 / 1024, 2)
    cpu_percent = psutil.cpu_percent(interval=0)

    list1 = []
    list2 = []
    for i in psutil.process_iter(attrs=['pid']):
        threads = psutil.Process(pid=i.pid).num_threads()
        list1.append(i.pid)
        list2.append(threads)
    system_info = {
        "cpu_usage": round(cpu_percent, 2),
        "cpu_process": len(list1),
        "cpu_thread": sum(list2),
        "cpu_time": psutil.cpu_times().idle,  # idle空闲时间
        "memory_used_memory": f'{round(used_memory, 2)}G',
        "memory_free_memory": f'{round(free_memory, 2)}G',
        "memory_usage": f'{round(memory_percent, 2) * 100:.2f}',
        'disk_percentage': round(percentage, 2),
        'disk_read_velocity': f'{(read / r_time):.2f}MB/s',
        'disk_write_velocity': f'{(write / w_time):.2f}MB/s',
    }
    return system_info


def check_ip(ip):
    if len(ip.split(':')) == 1:
        port = None
        return ip, port
    else:
        ip, port = ip.split(':')
        return ip, port

# server_port = {
#     21: 'FTP', 22: 'SSH', 23: 'TELNET', 25: 'SMTP', 53: 'DNS', 67: 'BOOTPS', 68: 'BOOTPC', 69: 'TFTP',
#     79: 'FINGER', 80: 'HTTP', 109: 'POP2', 110: 'POP3', 119: 'NNTP', 123: 'NTP', 135: 'EPMAP', 143: 'IMAP',
#     189: 'QFT', 213: 'IPX', 220: 'IMAP3', 389: 'LDAP', 433: 'NNSP', 443: 'HTTPS', 465: 'SMTPS', 469: 'RCP',
#     501: 'STMF', 576: 'IPCD', 993: 'IMAPS', 995: 'POP3S', 1433: 'MSSQL', 3306: 'MYSQL', 3389: 'RDP',
#     3421: 'BMAP', 6379:'REDIS',8000: 'IRDMI', 8080: 'WWW', 10000: 'NDMP'
# }
#
# port_server = {'FTP': 21, 'SSH': 22, 'TELNET': 23, 'SMTP': 25, 'DNS': 53, 'BOOTPS': 67, 'BOOTPC': 68, 'TFTP': 69,
#                'FINGER': 79, 'HTTP': 80, 'POP2': 109, 'POP3': 110, 'NNTP': 119, 'NTP': 123, 'EPMAP': 135, 'IMAP': 143,
#                'QFT': 189, 'IPX': 213, 'IMAP3': 220, 'LDAP': 389, 'NNSP': 433, 'HTTPS': 443, 'SMTPS': 465, 'RCP': 469,
#                'STMF': 501, 'IPCD': 576, 'IMAPS': 993, 'POP3S': 995, 'MSSQL': 1433, 'MYSQL': 3306, 'RDP': 3389,
#                'BMAP': 3421,'REDIS':6379, 'IRDMI': 8000, 'WWW': 8080, 'NDMP': 10000}
