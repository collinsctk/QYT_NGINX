### 前期环境准备, 关闭防火墙(firewalld)和selinux
- linux环境
- docker
- docker-compose
- 互联网
- openssl
- python3

```shell
yum install -y gcc python3.9 python39-devel git

ln -sb /usr/bin/python3.9 /usr/bin/python3
ln -sb /usr/bin/pip3.9 /usr/bin/pip3

yum install -y yum-utils device-mapper-persistent-data lvm2

yum-config-manager \
                  --add-repo \
                  http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

yum install -y docker-ce docker-ce-cli containerd.io

systemctl start docker
systemctl enable docker

pip3 install docker-compose

git clone https://github.com/collinsctk/QYT_NGINX.git

```
### 执行脚本产生证书与秘钥
```shell
# 进入cfssl目录
[root@localhost cfssl]# pwd
/QYT_NGINX/cfssl

# 客户输入域名, 产生证书与秘钥文件
[root@localhost cfssl]# python3 auto_cert.py
请输入域名:www.qytang.com
明文证书文件: /root/QYT_NGINX/cfssl/server.pem
明文秘钥文件: /root/QYT_NGINX/cfssl/server-key.pem
PKCS12加密打包后的文件:/root/QYT_NGINX/cfssl/www.qytang.com.p12
PKCS12加密密码为:Cisc0123

```

### 直接用docker-compose拉起镜像
```shell
# 进入docker-compose.yaml相同的目录
[root@localhost QYT_NGINX]# pwd
/QYT_NGINX
# 构建镜像
[root@localhost QYT_NGINX]# docker-compose build
# 拉起服务
[root@localhost QYT_NGINX]# docker-compose up -d

```

### 根证书介绍
```angular2html
# 根证书(有效期20年)
QYT_NGINX/cfssl/ca.cer

# 根证书的秘钥
QYT_NGINX/cfssl/ca-key.pem

```
