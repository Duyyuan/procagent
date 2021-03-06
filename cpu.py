# -*- encoding: utf-8 -*
# Copyright © 2013 Computer Network Information Center, Chinese Academy of Sciences
#
# Author: Jing Shao <jingshao@cnic.cn>

from collections import OrderedDict
import pprint
import util
import time

def CPUInfo():
    cpu_info = OrderedDict()
    proc_info = OrderedDict()

    nprocs = 0

    try:    
        if util.is_exist('/proc/cpuinfo'):
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if not line.strip():
                        cpu_info['proc%s' % nprocs] = proc_info
                        nprocs += 1
                        proc_info = OrderedDict()
                    else:
                        if len(line.split(':')) == 2:
                            proc_info[line.split(':')[0].strip()] = line.split(':')[1].strip()
                        else:
                            proc_info[line.split(':')[0].strip()] = ''
    except:
        print "Unexpected error:", sys.exc_info()[1]
    finally:    
        return cpu_info

def _read_proc_stat():
    cpu_line = OrderedDict()
    f = None

    try:
        if util.is_exist('/proc/stat'):
            f = open('/proc/stat')
            lines = f.readlines()
            for line in lines:
                if line.startswith('cpu'):
                    tmp = line.strip().split()
                    cpu_line[tmp[0]] = tmp[1:len(tmp)]
    except:
        print "Unexpected error: ", sys.exc_info[1]
    finally:
        if f:
            f.close()
        return cpu_line

def CPUUsage_all():
    cpu_usage = {}
    cpu_line = _read_proc_stat()
    total_1 = {}
    idle_1 = {}
    total_2 = {}
    idle_2 = {}

    if cpu_line:
        for item in cpu_line:
            total_1[item] = float(cpu_line[item][0]) + float(cpu_line[item][1]) + \
                    float(cpu_line[item][2]) + float(cpu_line[item][3]) + \
                    float(cpu_line[item][4]) + float(cpu_line[item][5]) + float(cpu_line[item][6])
            idle_1[item] = float(cpu_line[item][3])

        time.sleep(1)
        
        cpu_line_2 = _read_proc_stat()
 
        if cpu_line_2:
            for item in cpu_line_2:
                total_2[item] = float(cpu_line_2[item][0]) + float(cpu_line_2[item][1]) + \
                          float(cpu_line_2[item][2]) + float(cpu_line_2[item][3]) + \
                          float(cpu_line_2[item][4]) + float(cpu_line_2[item][5]) + float(cpu_line_2[item][6])
                idle_2[item] = float(cpu_line_2[item][3])

        if total_1 and total_2:
            for item in total_1:
                cpu_usage[item] = 100 * (1 - float(idle_2[item] - idle_1[item])/float(total_2[item] - total_1[item]))
    return cpu_usage       


def CPUUsage():
    cpu_usage = -1
    cpu_line = _read_proc_stat()
    total_1 = 0
    idle_1 = 0
    total_2 = 0
    idle_2 = 0

    if cpu_line:
        total_1 = float(cpu_line['cpu'][0]) + float(cpu_line['cpu'][1]) + \
                  float(cpu_line['cpu'][2]) + float(cpu_line['cpu'][3]) + \
                  float(cpu_line['cpu'][4]) + float(cpu_line['cpu'][5]) + float(cpu_line['cpu'][6])
        idle_1 = float(cpu_line['cpu'][3])

        time.sleep(1)
        cpu_line_2 = _read_proc_stat()
        if cpu_line_2:
            total_2 = float(cpu_line_2['cpu'][0]) + float(cpu_line_2['cpu'][1]) + \
                      float(cpu_line_2['cpu'][2]) + float(cpu_line_2['cpu'][3]) + \
                      float(cpu_line_2['cpu'][4]) + float(cpu_line_2['cpu'][5]) + float(cpu_line_2['cpu'][6])
            idle_2 = float(cpu_line_2['cpu'][3])

        if total_1 != 0 and total_2 != 0:
            cpu_usage = 100 * (1 - float(idle_2 - idle_1)/float(total_2 - total_1))
    return cpu_usage
        
if __name__=='__main__':
    print CPUUsage_all()
