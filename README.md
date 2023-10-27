# redis-py

A simplified Redis clone built using Python for educational purposes.

## Features

- [x] Basic TCP server
- [ ] Command parser
- [ ] GET, SET, DEL commands
- [ ] Persistence
- [ ] Multi-threading

## Getting Started

### Prerequisites

- Python 3.x
- git (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/redis-py.git
   ```

2. Navigate to the project directory:

   ```bash
   git clone https://github.com/your-username/redis-py.git
   ```

3. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

### Running the Server

1. Run the server from project root:

   ```bash
   python3 src/server.py
   ```

   The server will start and listen for incoming connections on **127.0.0.1:6379**.

### Testing with Telnet

Use Telnet to manually test the server.

1. Open a new terminal window.

2. Run the following:

```bash
telnet 127.0.0.1 6379
```

You can now type commands and see responses from the server.

## License

This project is licensed under the MIT License.
