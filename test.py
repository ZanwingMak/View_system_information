#coding:utf-8
__author__ = 'm9Kun'
import psutil
import datetime
import urllib2
import re
import time
import sys
import os

def get_my_ip():
    print u'正在联网查询您的ip地址...'
    url1 = 'http://ip.chinaz.com/'
    url2 = 'http://ip.dnsexit.com/'
    url3 = 'http://www.whereismyip.com/'
    my_ip = ''
    try:
        opener = urllib2.urlopen(url1,timeout=8)
        if url1 == opener.geturl():
            html = opener.read()
            my_ip = re.search('\d+\.\d+\.\d+\.\d+',html).group(0)
    except:
        try:
            opener = urllib2.urlopen(url2,timeout=10)
            if url2 == opener.geturl():
                html = opener.read()
                my_ip = re.search('\d+\.\d+\.\d+\.\d+',html).group(0)
        except:
            try:
                opener = urllib2.urlopen(url2,timeout=15)
                if url3 == opener.geturl():
                    html = opener.read()
                    my_ip = re.search('\d+\.\d+\.\d+\.\d+',html).group(0)
            except:
                print(u'联网查询外网ip失败...')
                my_ip = 'None'
    if my_ip != 'None':
        print(u'您的外(公)网ip是:' + my_ip)
        return my_ip

def process():
    all_process_pid = psutil.pids()
    print u'-------------------------------当前进程列表-------------------------------'
    print u'[PID]\t  [进程名]\t\t      [创建时间]\t\t[线程数]'
    print '--------------------------------------------------------------------------'
    for i in range(len(all_process_pid)):
        p = psutil.Process(all_process_pid[i])
        print u'%-10s%-28s%-20s\t%s' % (all_process_pid[i],p.name(),datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S"),p.num_threads())
    print '--------------------------------------------------------------------------'


def users():
    users_count = len(psutil.users())
    users_list = '、'.join([i.name for i in psutil.users()])
    print u"当前系统有%d个用户，分别有：%s"%(users_count,users_list)

def boot_time():
    #转换成自然时间格式
    print u'系统启动时间：%s' % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

def network():
    network = psutil.net_io_counters()
    sent = '%.2fm' % (network.bytes_sent/1024.0/1024.0)
    recv = '%.2fm' % (network.bytes_recv/1024.0/1024.0)
    print u"接收流量：%s 发送流量：%s"%(sent,recv)
    get_my_ip()

def disk():
    disk_partitions = psutil.disk_partitions()
    disk_len = len(disk_partitions)
    print u'[当前磁盘有%d个分区]' % disk_len
    for i in range(disk_len):
        print u'盘符：%s 挂载点：%s 文件系统：%s 属性：%s' % ((disk_partitions[i][0])[0:1],(disk_partitions[i][1])[0:1],disk_partitions[i][2],(disk_partitions[i][3]))
    disk_io_counters = psutil.disk_io_counters(perdisk=False)
    print u'磁盘读取IO个数：%d' % disk_io_counters.read_count
    print u'磁盘写入IO个数：%d' % disk_io_counters.write_count
    print u'磁盘读取IO字节数：%d B' % disk_io_counters.read_bytes
    print u'磁盘写入IO字节数：%d B' % disk_io_counters.write_bytes
    print u'磁盘读取时间：%s' % disk_io_counters.read_time
    print u'磁盘写入时间：%s' % disk_io_counters.write_time
    disk = psutil.disk_usage('/')
    print u'磁盘分区(不包括系统盘)总容量：%.2fG' % (disk.total/1024.0/1024.0/1024.0)
    print u'磁盘分区(不包括系统盘)已用空间：%.2fG' % (disk.used/1024.0/1024.0/1024.0)
    print u'磁盘分区(不包括系统盘)可用空间：%.2fG' % (disk.free/1024.0/1024.0/1024.0)
    print u'磁盘分区(不包括系统盘)空间占用率：%s%%' % disk.percent

def memory():
    memory = psutil.virtual_memory()
    print u'总内存：%.2fM' % (memory.total/1024.0/1024.0)
    print u'已使用内存：%.2fM' % (memory.used/1024.0/1024.0)
    print u'内存占用率：%s%%' % memory.percent
    print u'可用内存：%.2fM' % (memory.available/1024.0/1024.0)
    print u'空闲内存：%.2fM' % (memory.free/1024.0/1024.0)

def cpu():
    cpu_times_percent = psutil.cpu_times_percent()
    cpu_times = psutil.cpu_times()
    print u"CPU逻辑个数：%d" % psutil.cpu_count()
    print u"CPU物理个数：%d" % psutil.cpu_count(logical=False)
    print u'CPU时间比：[用户进程:%s  内核进程:%s  空闲(IDLE):%s]' % (cpu_times.user,cpu_times.system,cpu_times.idle)
    print u'CPU当前使用率：[用户进程:%s%%  内核进程:%s%%  空闲(IDLE):%s%%]' % (cpu_times_percent.user,cpu_times_percent.system,cpu_times_percent.idle)
    print u'CPU当前总使用率：%s%%' % psutil.cpu_percent()

def restart_program():  #重启程序
    python = sys.executable
    os.execl(python, python, * sys.argv)

def Main_Menu():
    print u'---------------------请选择需要查看的系统信息----------------------'
    print u'|    1.CPU 2.内存 3.磁盘 4.网络 5.开机时间 6.进程 7.用户 8.退出   |'
    print u'-------------------------------------------------------------------'
    select = raw_input()
    if select == '1':
        cpu()
    elif select == '2':
        memory()
    elif select == '3':
        disk()
    elif select == '4':
        network()
    elif select == '5':
        boot_time()
    elif select == '6':
        process()
    elif select == '7':
        users()
    elif select == '8':
        print u'正在退出...'
        quit()
    else:
        print u'输入错误，请重新输入！'

if __name__ == '__main__':
    print u'%s用户，您好!' % (psutil.users()[0][0])
    while True:
        Main_Menu()
