import ipaddress
import requests

# 远程 CIDR 列表地址
URL = "https://raw.githubusercontent.com/Loyalsoldier/geoip/refs/heads/release/text/cn.txt"
OUTPUT_FILE = "wildcard_output.txt"

def cidr_to_wildcard(cidr):
    try:
        # 解析CIDR网络地址
        network = ipaddress.IPv4Network(cidr, strict=False)
        # 获取子网掩码的每一部分（0-255），转换为整数
        netmask_parts = [int(octet) for octet in network.netmask.exploded.split(".")]

        # 将CIDR转换为通配符格式
        wildcard = ".".join(
            str(int(network.network_address.exploded.split(".")[i]) | (255 - netmask_parts[i]))
            if netmask_parts[i] != 255 else "*"
            for i in range(4)
        )

        return wildcard
    except ValueError:
        return f"Invalid CIDR: {cidr}"

def download_and_convert(url, output_file):
    try:
        # 获取远程CIDR列表
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果请求失败，抛出异常
        cidr_list = response.text.strip().split("\n")

        # 转换每个CIDR为通配符格式
        converted_list = [cidr_to_wildcard(cidr.strip()) for cidr in cidr_list if cidr.strip()]

        # 写入转换后的结果到文件
        with open(output_file, "w") as f:
            f.writelines("\n".join(converted_list) + "\n")

        print(f"✅ 转换完成，结果保存在 {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败: {e}")

if __name__ == "__main__":
    download_and_convert(URL, OUTPUT_FILE)
