import platform
import psutil

class OsInfo:
    def __init__(self):
        self.os = platform.system()
        self.release = platform.release()
        self.version = platform.version()
        self.architecture = platform.machine()


class CpuInfo:
    def __init__(self):
        self.physical_cores = psutil.cpu_count(logical=False)
        self.total_cores = psutil.cpu_count(logical=True)
        self.max_frequency = psutil.cpu_freq().max
        self.min_frequency = psutil.cpu_freq().min
        self.current_frequency = psutil.cpu_freq().current
    
    @property
    def cpu_usage(self):
        return psutil.cpu_percent(interval=1)

  
class MemoryInfo:
    def __init__(self):
        svmem = psutil.virtual_memory()
        self._total = svmem.total
        self._available = svmem.available
        self._used = svmem.used
        self.percent_used = svmem.percent
        
    @property
    def total(self):
        return self.bytes_to_readable(self._total)
    
    @property
    def available(self):
        return self.bytes_to_readable(self._available)
    
    @property
    def used(self):
        return self.bytes_to_readable(self._used)
    
    @staticmethod
    def bytes_to_readable(bytes, unit='GB'):
        """
        Convert bytes to a more readable format.
        
        :param bytes: The number of bytes.
        :param unit: The unit to convert to ('KB', 'MB', 'GB').
        :return: The converted value in the specified unit.
        """
        factor = 1024.0
        if unit == 'KB':
            return f"{bytes / factor:.2f} KB"
        elif unit == 'MB':
            return f"{bytes / (factor ** 2):.2f} MB"
        elif unit == 'GB':
            return f"{bytes / (factor ** 3):.2f} GB"
        else:
            return f"{bytes} bytes"  # Fallback to bytes if unit is not recognized


class PartitionInfo:
        def __init__(self, partition):
            usage = psutil.disk_usage(partition.mountpoint)
            self.mountpoint = partition.mountpoint
            self.total_size = usage.total
            self.used = usage.used
            self.free = usage.free
            self.percent_used = usage.percent


class DiskInfo:
    def __init__(self):
        self.partitions = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            self.partitions.append(PartitionInfo(partition))


class SystemInfo:
    def __init__(self):
        self.os_info = OsInfo()
        self.cpu_info = CpuInfo()
        self.memory_info = MemoryInfo()
        self.disk_info = DiskInfo()