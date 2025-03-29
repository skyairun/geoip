import requests
import netaddr

# 远程 CIDR 列表地址
URL = "https://raw.githubusercontent.com/Loyalsoldier/geoip/refs/heads/release/text/cn.txt"
OUTPUT_FILE = "wildcard_output.txt"

def cidr_to_wildcard(cidr):
    """
    利用 netaddr 将 CIDR 地址转换为通配符格式。
    例如： '36.56.0.0/13' 转换后为 '36.56-63.*.*'
    """
    try:
        # 使用 netaddr 内置方法进行转换
        ip_glob = netaddr.IPGlob.from_cidr(cidr)
        return str(ip_glob)
    except Exception as e:
        return f"Invalid CIDR: {cidr} ({e})"

def download_and_convert(url, output_file):
    try:
        # 从远程 URL 下载 CIDR 列表
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        cidr_list = response.text.strip().splitlines()

        # 将每个 CIDR 转换为通配符格式
        converted_list = [cidr_to_wildcard(cidr.strip()) for cidr in cidr_list if cidr.strip()]

        # 将转换结果写入输出文件
        with open(output_file, "w") as f:
            f.write("\n".join(converted_list) + "\n")

        print(f"✅ 转换完成，结果保存在 {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败: {e}")

if __name__ == "__main__":
    download_and_convert(URL, OUTPUT_FILE)
