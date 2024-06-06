#!/bin/bash

# 清除现有规则
iptables -F
iptables -X

# 设置默认策略
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 允许回环接口流量
iptables -A INPUT -i lo -j ACCEPT

# 允许已建立的连接和相关连接
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 允许特定的 IP 地址访问端口 443
iptables -A INPUT -p tcp -s 10.1.1.0/24 --dport 443 -j ACCEPT

# 拒绝其他所有的 TCP/443 流量
iptables -A INPUT -p tcp --dport 443 -j REJECT

# 启动 nginx
nginx -g 'daemon off;'
