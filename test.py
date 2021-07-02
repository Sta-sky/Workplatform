def monitor(frist_invoke=2):
    """
    Return (inbytes, outbytes, in_num, out_num, ioms) of disk.
    """
    sdiskio = psutil.disk_io_counters()
    # sleep some time

    value_dic = {
        'iostats': {
            'io.disks_read': sdiskio.read_bytes/(1024*1024),
            'io.disks_write': sdiskio.write_bytes/(1024*1024),
            'io.disks_read_count': sdiskio.read_count/(1024 * 1024),
            'io.disks_write_count': sdiskio.write_count/(1024 * 1024),
            'io.disks_read_time': sdiskio.read_time/1000,
            'io.disks_write_time': sdiskio.write_time/1000,
            'io.disks_busy_time': sdiskio.write_time/1000,
        }
    }
    return value_dic

