### 前期环境准备, 关闭防火墙(firewalld)和selinux
- linux环境
- docker
- docker-compose
- 互联网


### 执行脚本产生证书与秘钥
```shell
# 进入cfssl目录
[root@localhost cfssl]# pwd
/QYT_NGINX/cfssl

# 客户输入域名, 产生证书与秘钥文件
[root@localhost cfssl]# python3 auto_cert.py
请输入域名:www.qytang.com
证书文件被输出到: /QYT_NGINX/cfssl/server.pem
证书秘钥被输出到: /QYT_NGINX/cfssl/server-key.pem

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

### 证书介绍
```angular2html
# 根证书(有效期20年)
QYT_NGINX/cfssl/ca.cer

# 根证书的秘钥
QYT_NGINX/cfssl/ca-key.pem

```

# 如果想输出PKCS12格式的证书请使用如下命令
```shell
openssl pkcs12 -export -out server.p12 -inkey server-key.pem -in server.pem

```
