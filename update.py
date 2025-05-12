import netifaces
import socket
import yaml
import subprocess

def is_public_ipv6(ip):
    # 排除 ULA（fc00::/7）、回环、链路本地
    return not (
        ip.startswith('fe80') or
        ip.startswith('::1') or
        ip.startswith('fc') or
        ip.startswith('fd')
    )

def get_ipv6_addresses():
    ipv6_list = []
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET6 in addrs:
            for addr in addrs[netifaces.AF_INET6]:
                ip = addr['addr'].split('%')[0]
                if is_public_ipv6(ip):
                    ipv6_list.append(ip)
    return ipv6_list

def test_ipv6_connect(ip, port=22, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.close()
        return True
    except Exception:
        return False

def update_yaml_with_ipv6(yaml_path, new_ip):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    if 'server' in data and 'ip' in data['server']:
        data['server']['ip'] = new_ip
    with open(yaml_path, 'w') as f:
        yaml.safe_dump(data, f, allow_unicode=True)

ipv6_list = get_ipv6_addresses()
print("可用的IPv6地址：")
for ip in ipv6_list:
    print(f"{ip} 可连接: {test_ipv6_connect(ip)}")

# 取第一个可用IPv6地址，更新到yml
if ipv6_list:
    update_yaml_with_ipv6('ipv6_addresses.yml', ipv6_list[0])
    print(f"已将 {ipv6_list[0]} 更新到 ipv6_addresses.yml 的 workstation ip 字段")
else:
    print("未找到可用的IPv6地址")

def git_commit_and_push():
    status = subprocess.getoutput('git status --porcelain')
    if status.strip():
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', '自动检测并更新IPv6地址到yml'])
        subprocess.run(['git', 'push'])
        print('已提交并推送更改到远程仓库')
    else:
        print('没有需要提交的更改')

git_commit_and_push()

