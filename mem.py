# -*- coding: utf-8 -*-
# @Project: mi
# @File: mem.py
# @Author: kehr
# @Date: 2016-10-18 18:52:22
# @Email: kehr.china@gmail.com

class Memory(object):
    """System memory infomation
    All of unit of the function return value is kb
    """
    def __init__(self):
        self._mem_info = self.get_format_info()

    def get_format_info(self):
        """Convert the content of `/proc/meminfo` to a dict
           return a dict object
        """
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                items = line.strip().split()
                info[items[0].rstrip(":")] = int(items[1])

        return info

    def monitor(index, interval=1, count=10, timeout=60):
        """Monitor the index change
        Args:
            index: [MemFree| Cached| used]

        """
        pass

    def get_mem_total(self):
        """MemTotal"""
        return self._mem_info["MemTotal"]

    def get_mem_free(self):
        """MemFree + Cached + Buffers"""
        return self._mem_info["MemFree"] + \
               self._mem_info["Cached"] + \
               self._mem_info["Buffers"]

    def get_mem_used(self):
        """Calculate memory used
        MemTotal - MemFree - Buffers - Cached
        """
        return self._mem_info["MemTotal"] - \
               self._mem_info["MemFree"] - \
               self._mem_info["Buffers"] - \
               self._mem_info["Cached"]

    def get_mem_cached(self):
        """Cached"""
        return self._mem_info["Cached"]

    def get_mem_free_percent(self):
        """used_mem/total_mem"""
        return round(float(self.get_mem_used())/self.get_mem_total(), 2) * 100

    def get_mem_used_percent(self):
        """100 - free_percent"""
        return 100 - self.get_mem_free_percent()

if __name__ == "__main__":
    m = Memory()
    print m.get_mem_used()
