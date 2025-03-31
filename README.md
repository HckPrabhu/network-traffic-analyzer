# network-traffic-analyzer
"Real-time network traffic analyzer with intrusion detection, built using Python and Flask."


## 🚧 Project Status  
**This project is under active development.**  
- Core features (packet capture, basic IDS) are functional.  
- Expect breaking changes as new features are added.  
- Documentation and testing are incomplete.


# 🌐 Real-Time Network Traffic Analyzer with Intrusion Detection  
![Dashboard Demo](./screenshots/dashboard-demo.gif)  
*Monitor, detect, and visualize network threats in real time.*  

---

## 🚀 Features  
- **Live Packet Capture**: Analyze HTTP, TCP/UDP, and DNS traffic using Scapy.  
- **Custom IDS Rules**: Detect SYN floods, port scans, and suspicious payloads.  
- **Interactive Dashboard**: Visualize traffic patterns with Flask and Matplotlib.  
- **Real-Time Alerts**: SMS/Email notifications via Twilio (optional).  
- **SQLite Logging**: Store and query historical traffic data.  

---

## 🛠️ Installation  

### Prerequisites  
- Python 3.9+  
- Admin privileges (for packet capture)  

```bash
# Clone the repository
git clone https://github.com/HckPrabhu/network-traffic-analyzer.git
cd network-traffic-analyzer

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🖥️ Usage  

### Step 1: Start Packet Capture  
```bash
# Terminal 1 (requires admin rights for raw socket access)
sudo python analyzer/packet_analyzer.py
```

### Step 2: Launch Dashboard  
```bash
# Terminal 2
python analyzer/dashboard/app.py
```
Access the dashboard at: [http://localhost:5000](http://localhost:5000)  

---

### 🎯 Simulating Attacks  
Test the IDS with these scenarios:  

1. **Port Scan**  
   ```bash
   nmap -sS localhost
   ```

2. **SYN Flood** (install `hping3` first)  
   ```bash
   sudo hping3 -S -p 80 --flood 127.0.0.1
   ```

3. **Malicious Payload**  
   ```bash
   curl http://localhost -H "User-Agent: cmd.exe"
   ```

---

## 📂 Project Structure  
```bash
network-traffic-analyzer/
├── analyzer/               # Core analysis and detection logic
├── database/               # SQLite database (auto-created)
├── docs/                   # Architecture and contribution guides
├── screenshots/            # Demo images/GIFs
├── .env.example            # Template for environment variables
└── requirements.txt        # Python dependencies
```

---

## 🛡️ IDS Rules Implemented  
| Threat Type          | Detection Method                          | Threshold           |  
|----------------------|-------------------------------------------|---------------------|  
| Port Scanning        | SYN packets to multiple closed ports      | >15 SYN packets/sec |  
| DDoS Attack          | High traffic volume from a single IP      | >1000 packets/sec   |  
| Suspicious Payload   | Keywords like `cmd.exe` in HTTP headers   | Exact string match  |  

---

## 🔌 Enabling Twilio Alerts  
1. Create a free [Twilio account](https://www.twilio.com/try-twilio).  
2. Rename `.env.example` to `.env` and add your credentials:  
   ```ini
   TWILIO_SID=your_account_sid
   TWILIO_TOKEN=your_auth_token
   TWILIO_PHONE=+1234567890  # Your Twilio phone number
   ALERT_PHONE=+0987654321   # Your personal phone number
   ```  
3. Uncomment the Twilio code in `packet_analyzer.py`.  

---

## 🤝 Contributing  
Contributions are welcome! Please follow these steps:  
1. Fork the repository.  
2. Create a branch: `git checkout -b feature/your-feature`.  
3. Commit changes: `git commit -m "Add your feature"`.  
4. Push to the branch: `git push origin feature/your-feature`.  
5. Open a Pull Request.  

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for details.  

---

## 📜 License  
Distributed under the MIT License. See [LICENSE](./LICENSE) for details.  

---

## 💡 Acknowledgements  
- Packet capture powered by [Scapy](https://scapy.net/).  
- Dashboard built with [Flask](https://flask.palletsprojects.com/).  
- IDS rules inspired by [Suricata](https://suricata.io/).  


---
🤝 How to Contribute
We welcome contributors to shape this project’s future!


⚠️ Disclaimer
This tool is intended for educational/research purposes only.
Do not use in production environments. The developers assume no liability for misuse.

---



