from typing import Dict

def check_port_scan(packet, suspect_ips: Dict[str, int], trigger_alert):
    if TCP in packet and packet[TCP].flags == 'S':
        src_ip = packet[IP].src
        suspect_ips[src_ip] = suspect_ips.get(src_ip, 0) + 1
        if suspect_ips[src_ip] > 15:  # Threshold
            trigger_alert(src_ip, "Port Scan")
            suspect_ips[src_ip] = 0

def check_ddos(packet, suspect_ips: Dict[str, int], trigger_alert):
    if IP in packet:
        src_ip = packet[IP].src
        suspect_ips[src_ip] = suspect_ips.get(src_ip, 0) + 1
        if suspect_ips[src_ip] > 1000:  # Threshold for DDoS
            trigger_alert(src_ip, "DDoS Attack")
            suspect_ips[src_ip] = 0
