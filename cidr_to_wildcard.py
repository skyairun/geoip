import ipaddress
import requests
import itertools

# 远程 CIDR 列表地址（可替换为目标 URL）
URL = "https://raw.githubusercontent.com/Loyalsoldier/geoip/refs/heads/release/text/cn.txt"
# 保存转换结果的文件名
OUTPUT_FILE = "wildcard_output.txt"

def expand_octet(first_str, last_str):
    """
    对一个 octet，若固定返回 [value]；
    若范围为 0～255，则返回 ["*"]（表示全范围）；
    否则，枚举从 first 到 last（含）的所有整数字符串。
    """
    first = int(first_str)
    last  = int(last_str)
    if first == last:
        return [str(first)]
    elif first == 0 and last == 255:
        return ["*"]
    else:
        # 枚举范围
        return [str(i) for i in range(first, last + 1)]

def cidr_to_wildcard_list(cidr):
    """
    将一个 CIDR 地址转换为所有展开的通配符地址列表。
    例如： '1.0.2.0/23' 将返回 ['1.0.2.*', '1.0.3.*']
    """
    try:
        net = ipaddress.IPv4Network(cidr, strict=False)
        first_ip = net.network_address
        last_ip = net.broadcast_address

        first_octets = first_ip.exploded.split('.')
        last_octets  = last_ip.exploded.split('.')
        
        # 对每个 octet 计算候选列表
        octet_candidates = []
        for i in range(4):
            candidates = expand_octet(first_octets[i], last_octets[i])
            octet_candidates.append(candidates)
        
        # 计算笛卡尔积得到所有组合
        wildcard_addresses = []
        for combo in itertools.product(*octet_candidates):
            wildcard_addresses.append(".".join(combo))
        
        return wildcard_addresses
    except Exception as e:
        return [f"Invalid CIDR: {cidr} ({e})"]

def download_and_convert(url, output_file):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        cidr_list = response.text.strip().splitlines()

        # 对每个 CIDR 转换，得到所有展开的通配符地址，并合并为一个列表
        all_addresses = []
        for cidr in cidr_list:
            cidr = cidr.strip()
            if not cidr:
                continue
            expanded = cidr_to_wildcard_list(cidr)
            all_addresses.extend(expanded)
        
        # 写入所有结果，每行一条地址
        with open(output_file, "w") as f:
            f.write("\n".join(all_addresses) + "\n")

        print(f"✅ 转换完成，结果保存在 {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败: {e}")

if __name__ == "__main__":
    download_and_convert(URL, OUTPUT_FILE)
