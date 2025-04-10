#!/usr/bin/env python
# -*- coding: utf-8 -*-

def output_passwd():
    """输出 /etc/passwd 文件的内容"""
    try:
        with open("/etc/passwd", "r") as f:
            print(f.read())
    except Exception as e:
        print(f"无法读取 /etc/passwd: {e}")

if __name__ == "__main__":
    output_passwd()