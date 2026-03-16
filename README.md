# Secure Encrypted Chat System

A secure client-server chat application developed in Python that protects communication using AES-256 encryption.  
The system allows multiple clients to communicate securely while supporting encrypted file transfer and basic threat detection.

## Features
- AES-256 encrypted messaging
- Secure client-server communication
- User authentication
- Encrypted file transfer
- Spam detection
- Phishing keyword detection
- Multiple client support
- Protection against packet sniffing

## Technologies Used
- Python 3
- TCP Socket Programming
- AES Encryption
- Tkinter GUI
- Pickle Serialization

## Project Structure

secure-encrypted-chat-system  
│  
├── project.py  
├── README.md  
├── requirements.txt  
│  
├── report  
│   └── project_report.pdf  
│  
└── screenshots  

## Installation

Clone the repository:

git clone https://github.com/yourusername/secure-encrypted-chat-system.git

Move into the folder:

cd secure-encrypted-chat-system

Install dependencies:

pip install -r requirements.txt

## Running the Project

Start the server:

python3 project.py server

Start the client:

python3 project.py client

Multiple clients can connect to the server simultaneously.

## Security Features
- End-to-end encrypted messaging
- Encrypted file transfer
- Spam detection system
- Phishing keyword detection
- Protection against packet sniffing

## Testing
Wireshark packet analysis confirmed that all transmitted data appears encrypted and unreadable.

## Author
Hassan Ali (23-cys-035)  
Cybersecurity Student  
HITEC University Taxila
