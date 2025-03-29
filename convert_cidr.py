import ipaddress
import requests

# 远程 CIDR 列表地址
URL = "https://raw.githubusercontent.com/Loyalsoldier/geoip/refs/heads/release/text/cn.txt"
OUTPUT_FILE = "wildcard_output.txt"

def cidr_to_wildcard(cidr):
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        wildcard = ".".join(
            str(network.network_address + (255 - network.netmask[i])) if network.netmask[i] != 255 else "*" for i in range(4)
        )
        return wildcard
    except ValueError:
        return f"Invalid CIDR: {cidr}"

def download_and_convert(url, output_file):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    cidr_list = response.text.strip().split("\n")

    converted_list = [cidr_to_wildcard(cidr.strip()) for cidr in cidr_list if cidr.strip()]

    with open(output_file, "w") as f:
        f.writelines("\n".join(converted_list) + "\n")

    print(f"✅ 转换完成，结果保存在 {output_file}")

if __name__ == "__main__":
    download_and_convert(URL, OUTPUT_FILE)
