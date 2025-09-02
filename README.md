# ClipboardSync

A lightweight Python application that enables seamless clipboard synchronization between two machines on the same local network. Copy on one machine, paste on another - it's that simple!

## Features

- **Real-time clipboard synchronization** between two machines
- **Cross-platform support** for text and images
- **Secure local network communication** using Flask
- **Easy setup** with minimal configuration
- **Lightweight and efficient** resource usage

## Requirements

- Python 3.6 or higher
- Two machines on the same local network
- Windows (other platforms may work but are not officially supported)

## Installation

### 1. Download the Repository

Clone or download this repository on both machines:

```bash
git clone https://github.com/yourusername/clipboardsync.git
cd clipboardsync
```

### 2. Install Dependencies

Install the required Python packages on both machines:

```bash
pip install flask pyperclip pillow requests
```

### 3. Configure Network Settings

#### Find Your Machine's IP Address

On each machine, open Command Prompt and run:

```cmd
ipconfig
```

Look for the **IPv4 Address** under your active network connection (usually starts with 192.168.x.x or 10.x.x.x).

#### Create Environment Configuration

Create a `.env` file in the project directory and add the IP address of the **target machine** (the one you want to send clipboard updates to):

```
TARGET_IP=192.168.1.100
```

> **Note**: Each machine should have the other machine's IP in its `.env` file.

## Network Setup

### Test Connectivity

Before running the application, verify that both machines can communicate with each other:

```cmd
ping [other-machine-ip]
```

If the ping fails, you'll need to configure Windows Firewall.

### Configure Windows Firewall (If Required)

If ping requests are timing out, create a custom inbound rule on both machines:

#### Method 1: Windows Firewall GUI

1. Press `Win + R` and type `wf.msc`, then press Enter
2. Click **"Inbound Rules"** → **"New Rule"**
3. **Rule Type**: Select **"Custom"**
4. **Protocol**: Select **"ICMPv4"**
5. Click **"Customize"** → Select **"Specific ICMP types"** → Check **"Echo Request"**
6. **Scope**:
   - **Local IP**: "Any IP address"
   - **Remote IP**: "These IP addresses" → Add the other machine's IP
7. **Action**: "Allow the connection"
8. **Profile**: Check **"Private"** only
9. **Name**: "ClipboardSync Ping Allow"

#### Method 2: PowerShell (Alternative)

Run as Administrator and replace `192.168.1.X` with the other machine's IP:

```powershell
New-NetFirewallRule -DisplayName "ClipboardSync ICMP" -Direction Inbound -Protocol ICMPv4 -IcmpType 8 -RemoteAddress "192.168.1.X" -Action Allow -Profile Private
```

### Verify Network Setup

After configuring the firewall, test connectivity again:

```cmd
ping [other-machine-ip]
```

You should see successful ping responses.

## Usage

1. **Start the application** on both machines:
   ```bash
   python clipboardsync.py
   ```

2. **Copy content** on any machine (text, images, etc.)

3. **Paste on the other machine** - your clipboard content will be automatically synchronized!

## How It Works

ClipboardSync uses a client-server architecture where each machine runs both a Flask server (to receive clipboard updates) and a client (to send clipboard updates). When you copy content on one machine, it automatically sends the data to the configured target machine.

## Troubleshooting

### Common Issues

**"Connection refused" or "Target machine unreachable"**
- Verify both machines are on the same network
- Check that the IP addresses in `.env` files are correct
- Ensure Windows Firewall rules are properly configured
- Try pinging between machines to test connectivity

**"Module not found" errors**
- Make sure all required packages are installed: `pip install flask pyperclip pillow requests`

**Clipboard not syncing**
- Restart both applications
- Verify the Flask server is running on the target machine
- Check that the `.env` file contains the correct target IP

## Security Notes

- ClipboardSync is designed for trusted local networks only
- The application does not use encryption for data transmission
- Ensure your local network is secure before using this tool