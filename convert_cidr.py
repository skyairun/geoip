import ipaddress
import re

def cidr_to_wildcard(cidr):
    """
    将 CIDR 地址转换为通配符格式。
    例如: 192.168.1.0/24 -> 192.168.1.*
    """
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        wildcard = ".".join(str(network.network_address + (255 - network.netmask[i])) if network.netmask[i] != 255 else "*" for i in range(4))
        return f"{wildcard}"
    except ValueError:
        return f"Invalid CIDR: {cidr}"

def process_file(input_file, output_file):
    """
    读取 CIDR 地址文件，转换后写入新的文件。
    """
    with open(input_file, "r") as f:
        cidr_list = [line.strip() for line in f.readlines() if line.strip()]
    
    converted_list = [cidr_to_wildcard(cidr) for cidr in cidr_list]

    with open(output_file, "w") as f:
        f.writelines("\n".join(converted_list))

if __name__ == "__main__":
    process_file("cidr_input.txt", "cidr_output.txt")
