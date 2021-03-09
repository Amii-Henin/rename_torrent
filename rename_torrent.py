# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 作者：AMII
# 时间：20210310
# 更新内容：完善日志存储、已改种子避免重新命名导致出错

import datetime
import os
import re
import time
from bcoding import bdecode


alldirs = []
logpath = 'D:\Sources\PY\\rename_torrent\log\\'
logfilename = 'rename_torrent_log.json'
now = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))

def main():
    alldirs.append(rootpath)
    get_dirs(rootpath)
    get_dirs_check(alldirs)
    save_log(logpath + logfilename,now + ':{\n')
    for path in alldirs:
        rename(path)
    save_log(logpath + logfilename,'}\n')

def rename(path):
    files,nfiles,path_files = get_list(path)
    for x in range(len(files)):
        fname = ''
        save_log(logpath + logfilename,'    ["' + path_files[x] + '"')
        if (len(nfiles[x]) != 40):
            save_log(logpath + logfilename,',skip],\n')
            continue
        try:
            with open(path_files[x],'rb') as f:
                # ff = f.read()
                fname = bdecode(f.read())['info']['name']
                if type(fname) == bytes :
                    save_log(logpath + 'rename_torrent_errlog_' + now + '.txt',path_files[x] + ',【需要手动调整】\n')
                    save_log(logpath + logfilename,',【读取失败，需手动调errrrrrrrrrrrrrrrrr】],\n')
                    print ('\n【【【Error File】】】',path_files[x],'\n')    #运行出错，保留日志
                    continue
                # print (fname)
        except:
            save_log(logpath + 'rename_torrent_errlog_' + now + '.txt',path_files[x] + '\n')
            save_log(logpath + logfilename,',【errrrrrrrrrrrrrrrrr】],\n')
            print ('\n【【【Error File】】】',path_files[x],'\n')    #运行出错，保留日志
            continue
        new_name = str(fname) + '__' + files[x]
        try:
            if os.path.exists(path + '\\' + new_name):
                save_log(logpath + logfilename,',exists],\n')
                continue
            os.rename(path_files[x],path + '\\' + new_name)
        except:
            save_log(logpath + 'rename_torrent_errlog_' + now + '.txt',path_files[x] + '\n')
            save_log(logpath + logfilename,',【重命名errrrrrrrrrrrrrrrrr】],\n')
            print ('\n【【【Error File】】】',path_files[x],'\n')    #运行出错，保留日志
            continue
        save_log(logpath + logfilename,'"' + path + '\\' + new_name + '",Done~~],\n')
        print (new_name,'  OK~~')

def get_dirs(root_path):    #遍历目录
    dirs = os.scandir(root_path)
    # print (root_path)
    for x in dirs:
        if x.is_dir():
            if x.name != '$RECYCLE.BIN' and x.name != 'System Volume Information':
                alldirs.append(root_path + '\\' + x.name)
                get_dirs(root_path + '\\' + x.name)

def get_dirs_check(alldirs):
    if re.search('\\\\\\\\',alldirs[-1]):
        for x in range(len(alldirs)):
            temp = alldirs[x].replace('\\\\','\\')
            alldirs[x] = temp

def get_list(path):     #获取并返回目录下种子文件等
    all_files = os.listdir(path)
    rule = r"\.torrent$"
    path_file_list = []
    file_list = []
    nfile_list = []
    for files in all_files:
        if re.search(rule, files, re.IGNORECASE):
            file_list.append(files)
            nfile_list.append(os.path.splitext(files)[0])
            path_file_list.append(path + '\\' + files)
    return (file_list,nfile_list,path_file_list)

def save_log(logname,mess):     #写入日志
    with open (logname,'a+',encoding='utf-8') as f:
        f.write(mess)

if __name__ == '__main__':
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    rootpath = input('请输入文件夹地址：')
    main()
