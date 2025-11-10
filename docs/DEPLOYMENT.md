# Deployment Guide

This guide covers deploying the RAG system on Raspberry Pi 5 and other platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Raspberry Pi 5 Deployment](#raspberry-pi-5-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Considerations](#production-considerations)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Hardware Requirements

**Raspberry Pi 5:**
- Raspberry Pi 5 (4GB or 8GB RAM recommended)
- MicroSD card (16GB+ recommended)
- Power supply (5V/5A USB-C)
- Network connection (Ethernet or WiFi)

**Alternative Platforms:**
- Any Linux system with Docker support
- Minimum 2GB RAM
- 2GB free disk space

### Software Requirements

- Docker Engine 20.10+
- Docker Compose V2+
- Internet connection (for initial setup)

## Raspberry Pi 5 Deployment

### 1. Prepare Raspberry Pi OS

Install Raspberry Pi OS (64-bit) on your Raspberry Pi 5:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Verify installation
docker --version
docker compose version
```

### 2. Clone and Deploy

```bash
# Clone repository
git clone https://github.com/l0kifs/rag-system-rpi5.git
cd rag-system-rpi5

# Create environment file (optional)
cp .env.example .env
# Edit .env if you want to customize settings

# Start the system
docker compose up -d

# Check logs
docker compose logs -f
```

### 3. Verify Deployment

```bash
# Check if container is running
docker compose ps

# Test the API
curl http://localhost:8000/health

# Run example script
python examples/test_api.py
```

### 4. Configure Auto-start

To start the RAG system automatically on boot:

```bash
# Create systemd service
sudo tee /etc/systemd/system/rag-system.service > /dev/null <<EOF
[Unit]
Description=RAG System for Raspberry Pi 5
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/$USER/rag-system-rpi5
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
User=$USER

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable rag-system.service
sudo systemctl start rag-system.service
```

## Cloud Deployment

### Docker Hub

```bash
# Build and push to Docker Hub
docker build -t your-username/rag-system-rpi5:latest .
docker push your-username/rag-system-rpi5:latest

# On target machine
docker pull your-username/rag-system-rpi5:latest
docker compose up -d
```

### AWS EC2

1. Launch an EC2 instance (t2.medium or larger)
2. Install Docker and Docker Compose
3. Clone repository and deploy
4. Configure security groups to allow port 8000
5. Optional: Set up Elastic IP for stable access

### DigitalOcean

1. Create a Droplet with Docker pre-installed
2. SSH into droplet
3. Clone repository and deploy
4. Configure firewall to allow port 8000

## Production Considerations

### Security

1. **Use HTTPS:**
   ```yaml
   # Add nginx reverse proxy
   services:
     nginx:
       image: nginx:alpine
       ports:
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./certs:/etc/nginx/certs
   ```

2. **Environment Variables:**
   - Never commit `.env` files
   - Use secrets management for sensitive data
   - Rotate credentials regularly

3. **Network Security:**
   ```yaml
   # Restrict ports in docker-compose.yml
   ports:
     - "127.0.0.1:8000:8000"  # Only local access
   ```

### Performance Optimization

1. **Resource Limits:**
   ```yaml
   services:
     rag-app:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '2'
           reservations:
             memory: 1G
             cpus: '1'
   ```

2. **Swap Configuration (Raspberry Pi):**
   ```bash
   # Increase swap space
   sudo dphys-swapfile swapoff
   sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

3. **Model Caching:**
   - Models are cached after first download
   - Consider pre-downloading models in Dockerfile
   - Mount model cache as volume for persistence

### Backup and Recovery

1. **Backup ChromaDB data:**
   ```bash
   # Create backup
   docker compose exec rag-app tar czf /tmp/chroma-backup.tar.gz /data/chroma
   docker cp rag-system-rpi5:/tmp/chroma-backup.tar.gz ./backups/
   
   # Restore backup
   docker cp ./backups/chroma-backup.tar.gz rag-system-rpi5:/tmp/
   docker compose exec rag-app tar xzf /tmp/chroma-backup.tar.gz -C /
   ```

2. **Automated Backups:**
   ```bash
   # Add to crontab
   0 2 * * * cd /home/user/rag-system-rpi5 && ./scripts/backup.sh
   ```

### Scaling

For handling more traffic:

1. **Multiple Instances:**
   ```yaml
   services:
     rag-app:
       deploy:
         replicas: 3
   ```

2. **Load Balancer:**
   Add nginx or traefik as reverse proxy

3. **Database Optimization:**
   - Consider using a dedicated ChromaDB server
   - Implement caching layer (Redis)

## Monitoring

### Health Checks

```bash
# Manual check
./scripts/health_check.sh

# Automated monitoring
watch -n 30 ./scripts/health_check.sh
```

### Logs

```bash
# View logs
docker compose logs -f rag-app

# Save logs to file
docker compose logs rag-app > logs/rag-$(date +%Y%m%d).log

# Monitor resource usage
docker stats rag-system-rpi5
```

### Metrics

Consider adding:
- Prometheus for metrics collection
- Grafana for visualization
- Alert manager for notifications

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs

# Check Docker status
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker
```

### High Memory Usage

```bash
# Check memory
free -h

# Reduce top_k_results in .env
echo "TOP_K_RESULTS=3" >> .env

# Use smaller embedding model
echo "EMBEDDING_MODEL=all-MiniLM-L6-v2" >> .env
```

### Slow Response Times

1. First query is always slow (model loading)
2. Subsequent queries should be faster
3. Consider:
   - Reducing document count
   - Using smaller embedding model
   - Adding more RAM/swap

### Network Issues

```bash
# Check if port is open
sudo netstat -tlnp | grep 8000

# Check firewall
sudo ufw status

# Allow port
sudo ufw allow 8000/tcp
```

### Docker Disk Space

```bash
# Clean up unused resources
docker system prune -a

# Remove unused volumes
docker volume prune
```

## Updating

To update the RAG system:

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker compose up -d --build

# Or using Makefile
make restart
```

## Uninstalling

```bash
# Stop and remove everything
docker compose down -v

# Remove repository
cd ..
rm -rf rag-system-rpi5

# Optional: Remove Docker
sudo apt remove docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
