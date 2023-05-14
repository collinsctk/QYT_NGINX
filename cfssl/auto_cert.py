import subprocess
import os
import io
import json


# 执行系统命令的脚本
def system_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    proc.wait()
    stream_stdout = io.TextIOWrapper(proc.stdout)
    stream_stderr = io.TextIOWrapper(proc.stderr)

    str_stdout = str(stream_stdout.read())
    str_stderr = str(stream_stderr.read())

    return str_stdout, str_stderr


# 拷贝CFSSL相关文件, 并且给与执行权限
system_cmd('cp ./cfssl /usr/bin/cfssl')
system_cmd('cp ./cfssl-json /usr/bin/cfssl-json')
system_cmd('cp ./cfssl-certinfo /usr/bin/cfssl-certinfo')
system_cmd('chmod +x /usr/bin/cfssl*')

# 拷贝跟证书文件
system_cmd('mkdir -p /opt/certs')
system_cmd('cp ./ca-config.json /opt/certs/ca-config.json')
system_cmd('cp ./ca-csr.json /opt/certs/ca-csr.json')
system_cmd('cp ./ca.csr /opt/certs/ca.csr')
system_cmd('cp ./ca.cer /opt/certs/ca.cer')
system_cmd('cp ./ca-key.pem /opt/certs/ca-key.pem')

# 要求客户输入域名
input_domain = input('请输入域名:')

# 产生新的证书请求文件
cert_cer = {
    "CN": input_domain.strip(),
    "hosts": [input_domain.strip()],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "beijing",
            "L": "beijing",
            "O": "qytang",
            "OU": "qytangnetdevops"
        }
    ]
}

# 写入数据产生新的证书请求文件
with open('/opt/certs/server_request.json', 'w') as f:
    json.dump(cert_cer, f)

# os.chdir('/opt/certs')

# 产生证书
system_cmd('cfssl gencert -ca=/opt/certs/ca.cer -ca-key=/opt/certs/ca-key.pem '
           '-config=/opt/certs/ca-config.json -profile=server '
           '/opt/certs/server_request.json |cfssl-json -bare server')

# 拷贝证书与秘钥到NGINX目录
system_cmd('cp ./server-key.pem ../server.key')
system_cmd('cp ./server.pem ../server.crt')
system_cmd(f'openssl pkcs12 -export -out {input_domain.strip()}.p12 -inkey server-key.pem -in server.pem -passout pass:Cisc0123')
print(f'明文证书文件到: {os.getcwd()}/server.pem')
print(f'明文秘钥文件: {os.getcwd()}/server-key.pem')
print(f'PKCS12加密打包后的文件:{os.getcwd()}/{input_domain.strip()}.p12')
