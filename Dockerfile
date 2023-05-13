FROM rockylinux:8.5.20220308
#定义启动jenkins的用户
USER root

#修改时区为东八区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone

# 安装epel-release
RUN yum install -y epel-release

# 安装必要工具
RUN yum install -y nginx && yum install -y python3.8 && yum install -y gcc && yum install -y python38-devel && yum install -y net-tools && yum install -y bind-utils && yum install -y lrzsz && yum install -y curl && yum install -y dos2unix


ADD nginx.conf /etc/nginx/nginx.conf
ADD server.crt /etc/pki/nginx/server.crt
ADD server.key /etc/pki/nginx/private/server.key

# 拷贝目录
COPY static /usr/share/nginx/static
COPY html /usr/share/nginx/html

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]

