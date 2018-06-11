#!/usr/bin/env python
# coding=utf8

import os
import sys
import time

filter_name = None

'''
    simple script to filter the filename from the path which you input, the others would be deleted
    usage:
        pydelete.py   c:\test   a.txt
        which means to delete all files and directories at c:\test except a.txt file
'''


def recursion_delete_deep(path_prefix):
    if os.path.isdir(path_prefix):
        for obj in [os.path.join(path_prefix, i) for i in os.listdir(path_prefix)]:
            recursion_delete_deep(obj)
        if len(os.listdir(path_prefix)) == 0:
            os.rmdir(path_prefix)
            print("delete dir:" + path_prefix)
    else:
        basename = os.path.basename(path_prefix)
        if basename != filter_name:
            os.remove(path_prefix)
            print("delete file: " + path_prefix)
            
def recursion_delete_broad(*path_prefix):
    path_prefix = list(path_prefix)
    dnode_lists = []
    i = 0
    while i < len(path_prefix):
        k = path_prefix[i]
        if os.path.isdir(k):
            i += 1
            dnode_lists.extend([os.path.join(k, i) for i in os.listdir(k)])
        else:
            path_prefix.pop(i)
            basename = os.path.basename(k)
            if basename != filter_name:
                os.remove(k)
                print("delete file: " + k)
    if len(dnode_lists) != 0:
        recursion_delete_broad(*dnode_lists)
    for k in path_prefix:
        if len(os.listdir(k)) == 0:
            os.rmdir(k)
            print("delete dir:" + k)
    
def iteration_delete_deep(path_prefix):
    visited_nodes = []
    node_lists = [path_prefix]
    while len(node_lists) != 0:
        node = os.path.join(*node_lists)
        if node not in visited_nodes:
            visited_nodes.append(node)
        if os.path.isdir(node):
            flag = True
            for i in os.listdir(node):
                child_node = node_lists + [i]
                child_path = os.path.join(*child_node)
                if child_path not in visited_nodes:
                    flag = False
                    node_lists.append(i)
                    break
            if flag:
                node_lists.pop()
                if len(os.listdir(node)) == 0:
                    os.rmdir(node)
                    print("delete dir: " + node)
        else:
            basename = os.path.basename(node)
            if basename != filter_name:
                os.remove(node)
                print("delete file: " + node)
            node_lists.pop()
    
def iteration_delete_broad(path_prefix):
    node_lists = [path_prefix]
    dnode_list = []
    while len(node_lists) != 0:
        node = node_lists.pop(0)
        if os.path.isdir(node):
            dnode_list.append(node)
            for obj in [os.path.join(node, i) for i in os.listdir(node)]:
                node_lists.append(obj)
        else:
            basename = os.path.basename(node)
            if basename != filter_name:
                os.remove(node)
                print("delete file: " + node)
    for dnode in dnode_list[::-1]:
        if len(os.listdir(dnode)) == 0:
            os.rmdir(dnode)
            print("delete dir: " + dnode)
    
def interface_action(path_prefix):
    # for i in [os.path.join(path_prefix, p) for p in os.listdir(path_prefix)]:
        # recursion_delete_deep(i)
        
        
    for i in [os.path.join(path_prefix, p) for p in os.listdir(path_prefix)]:
        recursion_delete_broad(i)
        
        
    # for i in [os.path.join(path_prefix, p) for p in os.listdir(path_prefix)]:
        # iteration_delete_deep(i)
        
        
    # for i in [os.path.join(path_prefix, p) for p in os.listdir(path_prefix)]:
        # iteration_delete_broad(i)
    
def main():
    global filter_name
    
    path_prefix = None

    print(sys.argv)
    if len(sys.argv) != 3:
        print("exit 1")
        sys.exit(1)
        
    path_prefix = sys.argv[1]
    filter_name = sys.argv[2]
    
    if not os.path.exists(path_prefix):
        print("exit 2")
        sys.exit(2)
    
    interface_action(path_prefix)
    
if __name__ == "__main__":
    main()







