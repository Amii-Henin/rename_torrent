# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 作者：AMII
# 时间：20220211
# 更新内容：无法识别种子名也补上哈希值

import os
import re
import time
import base64
import magneturi
from bcoding import bdecode


logfile = r'D:\Sources\PY\rename_torrent\log\rename_torrent_log.json'
now = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))


def start(path):
    file_list,path_list = get_list(path)        # 获取文件、目录列表
    for f in file_list:                         # 循环文件列表
        rename(f,path)
    if len(path_list):                          # 如本级有目录则循环递归调用
        for p in path_list:
            start(p)


def rename(file,path):
    new_name = ''
    chk = re.search('_\w{32}_',file)
    if chk:
        save_log(logfile,'"' +os.path.join(path,file) + ',skip"')
        return True
    fname,b32hash,b16hash = get_torrent_name(os.path.join(path,file))       # 获取种子名及哈希值
    nfile = file.replace('.torrent','')
    nfile_chk = re.search('__\w{40}',nfile)             # 查找旧版程序命名
    if nfile_chk:
        nfile = nfile.replace(nfile_chk.group(),'')     # 移除旧版程序命名
    if nfile == str(fname) or nfile == b32hash or nfile == b16hash:         # 判断原文件名是否重复
        new_name = str(fname) + '_' + b32hash + '_' + b16hash + '.torrent'
    else:
        new_name = nfile + '_' + str(fname) + '_' + b32hash + '_' + b16hash + '.torrent'
        for rep in '\\/<>:"*?|':        # 替换特殊字符
            new_name = new_name.replace(rep,'_')
        if len(new_name) > 255:
            new_name = str(fname) + '_' + b32hash + '_' + b16hash + '.torrent'
        for rep in '\\/<>:"*?|':        # 替换特殊字符
            new_name = new_name.replace(rep,'_')
    try:
        if os.path.exists(path + '\\' + new_name):      # 如已存在则删除原种子
            save_log(logfile,'"' + os.path.join(path,file) + ',exists"')
            os.remove(os.path.join(path,file))
            return True
        os.rename(os.path.join(path,file),os.path.join(path,new_name))
    except:
        save_log(logfile,'【重命名errrrrrrrrrrrrrrrrr】,' + os.path.join(path,file))
        print ('\n【【【Error File】】】',os.path.join(path,file),'\n')    #运行出错，保留日志
        return False
    save_log(logfile,'"' + os.path.join(path,file) + ',' + new_name + ',Done~~"')
    print ('DONE ', new_name)

def get_torrent_name(path_file):
    with open(path_file,'rb') as f:
        try:
            metadata = magneturi.from_torrent_file(path_file)
            b32hash = re.search('(?<=btih:)\w{32}',metadata).group()
            b16hash = base64.b16encode(base64.b32decode(b32hash)).decode('utf-8')
            fname = bdecode(f.read())['info']['name']
            if type(fname) == bytes :
                save_log(logfile, '【读取失败，需手动调errrrrrrrrrrrrrrrrr】,' + path_file)
                print ('\n【【【Error File】】】',path_file,'\n')    #运行出错，保留日志
                return '',b32hash,b16hash
        except:
            save_log(logfile, '【errrrrrrrrrrrrrrrrr】' + path_file)
            print ('\n【【【Error File】】】',path_file,'\n')    #运行出错，保留日志
        return fname,b32hash,b16hash

def get_list(path):
    file_list = []
    path_list = []
    rule = r"\.(torrent)$"
    lists = os.listdir(path)
    for p in lists:
        if re.search("\$RECYCLE\.BIN|System Volume Information|Recovery",p): continue   # 排除windows系统文件夹
        if os.path.isdir(os.path.join(path,p)):
            path_list.append(os.path.join(path,p))      # 追加文件夹
            continue
        if re.search(rule, p, re.IGNORECASE):
            file_list.append(p)                         # 追加文件
    return (file_list, path_list)

def save_log(logname,mess):     #写入日志
    with open (logname,'a+',encoding='utf-8') as f:
        f.write(mess + '\n')

if __name__ == '__main__':
    if not os.path.exists(os.path.split(logfile)[0]):
        os.makedirs(os.path.split(logfile)[0])
    rootpath = input('请输入文件夹地址：') or "D:\Downloads\\temp"
    save_log(logfile,'\t' + now + ' ' + rootpath + ':')
    start(rootpath)
