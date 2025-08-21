# CN Lab (MA3105) Assignment 1 — Socket Programming

## 📌 Objective
Implement a TCP-based client-server application where:
- The client sends its **name** and an **integer (1–100)** to the server.
- The server responds with its **name** and its own **integer (1–100)**.
- Both client and server display the exchanged values and compute the **sum**.

### ⚠️ Caution
This `README` file was **AI-generated**.  (cause i hate writing readme.md by my own...)

---

## 🖥️ Features
- TCP client and server implemented in **Python**.
- Binary protocol using `struct` (`!H` for string length, `!I` for integer).
- Proper socket cleanup on exit.
- Server shuts down if invalid integer (outside 1–100) is received.
- **Concurrent server** using `threading.Thread`.
- **Logging** for better debugging and visibility.

---

## 📂 Files
- `server.py` — TCP server code
- `client.py` — TCP client code
- `cnlab1.pdf` — The Assignment File

---

## ▶️ How to Run

### 1. Start the Server
```bash
python server.py
```
- Enter an integer between `1–100` when prompted (this is the server’s number).
- The server listens on `0.0.0.0:8080` by default (all interfaces).
- The log will also show your local IP so clients can connect.

### 2. Start the Client
```bash
python client.py
```
- Enter an integer between `1–100` when prompted (this is the client’s number).
- The client will connect to the server, send its name and number, and receive the server’s response.
- Both sides compute and display the sum.

---

## 📡 Protocol
- **Message Format (Client → Server):**
  - `!H` → unsigned short (2 bytes) → length of client name  
  - `<name>` → UTF-8 encoded string  
  - `!I` → unsigned int (4 bytes) → client integer  

- **Message Format (Server → Client):**
  - `!H` → unsigned short (2 bytes) → length of server name  
  - `<name>` → UTF-8 encoded string  
  - `!I` → unsigned int (4 bytes) → server integer  

---

## 🔗 Interoperability Test
- You can test your client with a classmate’s server or vice versa (as required in the assignment).
- Works on the same machine (localhost) or across machines on the same network (using server’s IP).

---

## 🛠️ Notes
- Uses **port 8080** (can be changed in code).
- Requires **Python 3.9+** (for type hints like `list[threading.Thread]`).
- Close all sockets before re-running to avoid “port already in use” errors.
- Server will **terminate** if a client sends an invalid number.