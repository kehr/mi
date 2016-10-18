# -*- coding: utf-8 -*-
# @Project: mi
# @File: cpu.py
# @Author: kehr
# @Date: 2016-10-18 19:12:32
# @Email: kehr.china@gmail.com
# Description: Get the cpu infos. such as current cpuidle, cpu cores number(logical/physical)
# and if hyper theading enabled.

import time

class CPU(object):
    """System CPU information"""
    def __init__(self):
        self._logical_cores = 0
        self._physical_cores = 0
        self._siblings_num = 0
        self._cores_num = 0
        self._ht_enabled = 0
        self._cpu_info = self.get_cpu_info()
        self._stat_info = self.get_stat_info()

    def get_cpu_info(self):
        """Convert the content of `/proc/cpuinfo` to a dict
           return a dict object
        """
        info = {}
        physical_cores = set()
        cpu_cores = set()
        siblings = set()
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("processor"):
                    self._logical_cores += 1
                elif line.startswith("physical id"):
                    physical_cores.add(line.split()[-1])
                elif line.startswith("cpu cores"):
                    cpu_cores.add(line.split()[-1])
                elif line.startswith("siblings"):
                    siblings.add(line.split()[-1])
        self._ht_enabled = False if len(cpu_cores) == len(siblings) else True
        self._physical_cores = len(physical_cores)

    def get_stat_info(self):
        """Convert the content of `/proc/stat` to a dict
           return a dict object
        """
        info = {}
        with open("/proc/stat") as f:
            for line in f:
                if line.startswith("cpu"):
                    items = line.strip().split()
                    info[items[0]] = items[1:]
        return info

    def is_ht_enabled(self):
        """If the machine enable hyper threading modal"""
        return self._ht_enabled

    def get_physical_cores(self):
        """Get cpu physical cores number"""
        return self._physical_cores

    def get_logical_cores(self):
        """Get cpu logical cores number"""
        return self._logical_cores

    def get_idle(self, offset=3):
        """Get cpuidle percent
        Grab the idle value per `offset` seconds
        """
        prev_total, prev_idle = self._get_current_idle()
        # wait to get cpu info for the next time
        time.sleep(offset)
        total, idle = self._get_current_idle()
        diff_total = total - prev_total
        diff_idle = idle - prev_idle
        return round(float(diff_idle)/diff_total, 3) * 100

    def _get_current_idle(self):
        """Get current idle value and totle value"""
        stat = self.get_stat_info()
        idle = int(stat["cpu"][3])
        total = 0
        for value in stat["cpu"]:
            total += int(value)
        return (total, idle)


if __name__ == "__main__":
    import json
    cpu = CPU()
    while True:
        print cpu.get_idle(1)
