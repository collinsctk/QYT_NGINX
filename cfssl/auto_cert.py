import subprocess
import os
import io
import json


def system_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    proc.wait()
    stream_stdout = io.TextIOWrapper(proc.stdout)
    stream_stderr = io.TextIOWrapper(proc.stderr)

    str_stdout = str(stream_stdout.read())
    str_stderr = str(stream_stderr.read())

    return str_stdout, str_stderr


print(system_cmd('cp ./cfssl /usr/bin/cfssl'))
print(system_cmd('cp ./cfssl-json /usr/bin/cfssl-json'))
print(system_cmd('cp ./cfssl-certinfo /usr/bin/cfssl-certinfo'))
print(system_cmd('chmod +x /usr/bin/cfssl*'))

system_cmd('mkdir -p /opt/certs')
system_cmd('cp ./ca-config.json /opt/certs/ca-config.json')
system_cmd('cp ./ca-csr.json /opt/certs/ca-csr.json')
system_cmd('cp ./ca.csr /opt/certs/ca.csr')
system_cmd('cp ./ca.pem /opt/certs/ca.pem')
system_cmd('cp ./ca-key.pem /opt/certs/ca-key.pem')

input_domain = input('请输入域名:')

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

with open('/opt/certs/server_request.json', 'w') as f:
    json.dump(cert_cer, f)

# os.chdir('/opt/certs')

system_cmd('cfssl gencert -ca=/opt/certs/ca.pem -ca-key=/opt/certs/ca-key.pem '
           '-config=/opt/certs/ca-config.json -profile=server '
           '/opt/certs/server_request.json |cfssl-json -bare server')

system_cmd('cp ./server-key.pem ../server.key')
system_cmd('cp ./server.pem ../server.crt')
print(f'证书文件被输出到: {os.getcwd()}/server.pem')
print(f'证书秘钥被输出到: {os.getcwd()}/server-key.pem')