FROM python:3.12

WORKDIR /server

# Copy requirement files
COPY requirements.txt server.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies for Nmap, Impacket, and other tools
RUN apt-get update && apt-get install -y \
    nmap \
    smbclient \
    && rm -rf /var/lib/apt/lists/*

# Install additional Python libraries
RUN pip install --no-cache-dir \
    sublist3r \
    kuro \
    impacket

# Run the server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
