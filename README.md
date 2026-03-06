# 🔍 PrettyScan

**PrettyScan** is a visual web framework for network scanning, designed to produce clean, professional output suitable for corporate reports.

Built with Python (Flask) on the backend and a dark-themed dashboard UI on the frontend.

---

## ✨ Features

- 🖥 Web interface running on `localhost:5000`
- ⚡ Scan presets: common ports, full scan, vuln scan, OS detection, UDP, banners
- 📊 Dashboard with live stats (active hosts, open ports, duration)
- 🎨 Per-host cards with port table and risk classification (CRITICAL / HIGH / MEDIUM / LOW)
- 🌐 ES / EN language toggle (full interface translation)
- 📸 Export each host card as a PNG image (download or copy to clipboard)
- 📱 Responsive layout for small screens

---

## 🚀 Installation

### Requirements

- Python 3.8+
- nmap installed on the system

```bash
# Install nmap (Debian/Ubuntu/Kali)
sudo apt install nmap

# Install Python dependencies
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Then open your browser at: **http://localhost:5000**

---

## 🛠 Usage

1. Enter a target (IP, hostname or CIDR range) in the input field
2. Select scan options or use one of the presets
3. Click **Scan**
4. Once results appear, use the **⬇ Image** or **📋 Copy** buttons on each host card to export

---

## 📁 Project Structure

```
prettyscan/
├── app.py            # Flask backend + embedded frontend
├── requirements.txt  # Python dependencies
├── .gitignore
└── README.md
```

---

## ⚠️ Legal Notice

PrettyScan is intended for use on networks and systems you own or have explicit permission to scan. Unauthorized scanning may be illegal. Use responsibly.

---

## 📄 License

MIT License — feel free to use, modify and distribute.
