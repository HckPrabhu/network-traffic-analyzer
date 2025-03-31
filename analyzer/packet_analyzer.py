from scapy.all import AsyncSniffer, TCP, UDP, IP
from typing import Optional, Dict
import sqlite3
import time
from ids_rules import check_port_scan, check_ddos

class TrafficAnalyzer:
    def __init__(self):
        self.sniffer: Optional[AsyncSniffer] = None
        self.conn = sqlite3.connect('database/traffic.db')
        self._init_db()
        self.suspect_ips: Dict[str, int] = {}

    def _init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS traffic
                    (timestamp REAL, src_ip TEXT, dst_ip TEXT, 
                     src_port INTEGER, dst_port INTEGER, 
                     protocol TEXT, length INTEGER, flags TEXT)''')
        self.conn.commit()

    def _packet_handler(self, packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = packet[IP].proto
            src_port = dst_port = flags = None

            if TCP in packet:
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                flags = str(packet[TCP].flags)
            elif UDP in packet:
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport

            # Log to DB
            c = self.conn.cursor()
            c.execute('INSERT INTO traffic VALUES (?,?,?,?,?,?,?,?)',
                     (time.time(), src_ip, dst_ip, src_port, dst_port,
                      proto, len(packet), flags))
            self.conn.commit()

            # Run IDS checks
            check_port_scan(packet, self.suspect_ips, self._trigger_alert)
            check_ddos(packet, self.suspect_ips, self._trigger_alert)

    def _trigger_alert(self, ip: str, alert_type: str):
        print(f"ALERT: {alert_type} detected from {ip}")
        # Uncomment to enable Twilio alerts (add credentials in .env)
        # from twilio.rest import Client
        # account_sid = os.getenv('TWILIO_SID')
        # auth_token = os.getenv('TWILIO_TOKEN')
        # client = Client(account_sid, auth_token)
        # client.messages.create(
        #     body=f"ALERT: {alert_type} from {ip}",
        #     from_='+1234567890',
        #     to='+0987654321'
        # )

    def start(self):
        self.sniffer = AsyncSniffer(prn=self._packet_handler, store=False)
        self.sniffer.start()

    def stop(self):
        if self.sniffer:
            self.sniffer.stop()
            self.conn.close()

if __name__ == "__main__":
    analyzer = TrafficAnalyzer()
    try:
        analyzer.start()
        input("Press Enter to stop...\n")
    finally:
        analyzer.stop()
