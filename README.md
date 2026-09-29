# Secure Encrypted Chat System

A Python client-server chat application with a Tkinter interface. The project combines TCP socket programming, encrypted messaging, authentication, encrypted file transfer, and basic spam/phishing detection.

## Features

- AES-based encrypted messaging
- Client-server communication over TCP sockets
- User authentication
- Encrypted file transfer
- Multiple-client support
- Spam detection
- Phishing-keyword detection
- Tkinter graphical interface

## Technologies

- Python 3
- TCP sockets
- AES encryption
- Tkinter
- Pickle-based message serialization

## Requirements

Install the dependencies listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## Run

Clone the repository and enter its directory:

```bash
git clone https://github.com/hassanali-30/secure-encrypted-chat-system.git
cd secure-encrypted-chat-system
```

Start the server:

```bash
python3 project.py server
```

Start a client in another terminal:

```bash
python3 project.py client
```

Use `python` instead of `python3` on Windows if that is the command configured for Python 3.

## Project Structure

```text
project.py              # Client and server application
requirements.txt        # Python dependencies
report/                 # Project report, if present
screenshots/            # Demonstration images, if present
README.md               # Project documentation
```

## Security Note

This is an educational project. Review key management, authentication, serialization, and transport protections carefully before using it with real or sensitive communications.