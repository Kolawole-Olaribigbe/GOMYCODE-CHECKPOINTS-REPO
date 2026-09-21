# Docker Checkpoint

A hands-on Docker checkpoint covering container management, Dockerfiles, image creation, persistent storage, container networking, and Docker Compose.

## Objectives

This checkpoint demonstrates the ability to:

* Use the Docker CLI to manage containers and images
* Build custom Docker images with Dockerfiles
* Persist container data using Docker volumes
* Configure container-to-container communication using custom Docker networks
* Build and manage multi-container applications with Docker Compose

---

## Prerequisites

* Docker installed and running
* Docker Hub access for pulling official images
* Linux/WSL terminal
* Basic command-line knowledge

Verify Docker:

```bash
docker --version
```

Verify Docker Compose:

```bash
docker.compose version
```

> **Note:** This environment uses `docker.compose` for Compose commands rather than the older `docker-compose` command.

---

# 1. Docker Basics & CLI

## 1.1 Pull the Nginx Image

```bash
docker pull nginx
```

Verify the image:

```bash
docker images
```

## 1.2 Run Nginx

Run Nginx in detached mode and map host port `8080` to container port `80`:

```bash
docker run -d --name nginx-checkpoint -p 8080:80 nginx:latest
```

Verify:

```bash
docker ps
```

Open:

```text
http://localhost:8080
```

Expected result: the Nginx welcome page.

## 1.3 Inspect the Nginx HTML Directory

```bash
docker exec nginx-checkpoint ls -la /usr/share/nginx/html
```

Expected files include:

```text
50x.html
index.html
```

Enter the container:

```bash
docker exec -it nginx-checkpoint /bin/bash
```

View the default page:

```bash
cat /usr/share/nginx/html/index.html
```

Exit:

```bash
exit
```

## 1.4 Restart the Container

```bash
docker restart nginx-checkpoint
```

Verify:

```bash
docker ps
```

The container should remain available with the same port mapping.

## 1.5 Remove the Container and Image

Remove the checkpoint container:

```bash
docker rm -f nginx-checkpoint
```

Remove the `nginx:latest` image:

```bash
docker rmi nginx:latest
```

Verify:

```bash
docker images nginx
```

---

# 2. Docker Images & Dockerfiles

Directory:

```text
02-dockerfile/
```

Structure:

```text
02-dockerfile/
├── Dockerfile
├── app.py
└── requirements.txt
```

## 2.1 Application

### `app.py`

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from my custom Docker image!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### `requirements.txt`

```text
Flask
```

## 2.2 Dockerfile

### `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
```

## 2.3 Build the Image

From inside `02-dockerfile`:

```bash
docker build -t my-python-app:v1 .
```

Verify:

```bash
docker images my-python-app
```

## 2.4 Run the Application

```bash
docker run -d --name my-python-app -p 5000:5000 my-python-app:v1
```

Test:

```bash
curl http://localhost:5000
```

Expected:

```text
Hello from my custom Docker image!
```

## 2.5 Inspect Image History

```bash
docker history my-python-app:v1
```

This displays the image layers created from the Dockerfile.

Clean up the container:

```bash
docker rm -f my-python-app
```

> Keep the `my-python-app:v1` image if you want to inspect it later.

---

# 3. Docker Volumes & Storage

## 3.1 Create a Docker Volume

```bash
docker volume create mysql-checkpoint-data
```

Verify:

```bash
docker volume ls
```

## 3.2 Start MySQL with the Volume

```bash
docker run -d --name mysql-volume-checkpoint \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=checkpointdb \
  -v mysql-checkpoint-data:/var/lib/mysql \
  mysql:8.0
```

Verify:

```bash
docker ps
```

## 3.3 Connect to MySQL

```bash
docker exec -it mysql-volume-checkpoint mysql -uroot -prootpass checkpointdb
```

Create a table:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```

Insert test data:

```sql
INSERT INTO users (name) VALUES ('Kolawole');
```

Verify:

```sql
SELECT * FROM users;
```

Expected:

```text
+----+----------+
| id | name     |
+----+----------+
|  1 | Kolawole |
+----+----------+
```

Exit MySQL:

```sql
exit
```

## 3.4 Remove the Original Container

Stop:

```bash
docker stop mysql-volume-checkpoint
```

Remove:

```bash
docker rm mysql-volume-checkpoint
```

The volume must remain.

## 3.5 Recreate the Container Using the Same Volume

```bash
docker run -d --name mysql-volume-checkpoint-2 \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=checkpointdb \
  -v mysql-checkpoint-data:/var/lib/mysql \
  mysql:8.0
```

Connect again:

```bash
docker exec -it mysql-volume-checkpoint-2 mysql -uroot -prootpass checkpointdb
```

Verify the existing data:

```sql
SELECT * FROM users;
```

Expected:

```text
+----+----------+
| id | name     |
+----+----------+
|  1 | Kolawole |
+----+----------+
```

This confirms that the data persisted after the original container was removed.

---

# 4. Docker Networking

## 4.1 Create a Custom Network

```bash
docker network create internal-net
```

## 4.2 Test Container-to-Container Communication

Start the first Nginx container:

```bash
docker run -d \
  --name network-container-1 \
  --network internal-net \
  nginx:alpine
```

Start the second:

```bash
docker run -d \
  --name network-container-2 \
  --network internal-net \
  nginx:alpine
```

Test communication using the container name:

```bash
docker exec network-container-2 curl http://network-container-1
```

The Nginx welcome page should be returned.

This demonstrates Docker's internal DNS/service discovery.

## 4.3 Simple Application Networking Test

Directory:

```text
04-networking/
```

### `app.py`

```python
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = b"Hello from the networking test app!"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)


server = HTTPServer(("0.0.0.0", 5000), Handler)
print("Server running on port 5000")
server.serve_forever()
```

Run the application container:

```bash
docker run -d \
  --name network-app \
  --network internal-net \
  -v "$(pwd)":/app \
  -w /app \
  python:3.12-slim \
  python app.py
```

Run the client container:

```bash
docker run -d \
  --name network-client \
  --network internal-net \
  python:3.12-slim \
  sleep infinity
```

Test communication:

```bash
docker exec network-client python -c "import urllib.request; print(urllib.request.urlopen('http://network-app:5000').read().decode())"
```

Expected:

```text
Hello from the networking test app!
```

Clean up the temporary containers:

```bash
docker rm -f network-app network-client
```

---

# 5. Docker Compose

Directory:

```text
05-compose/
```

Structure:

```text
05-compose/
├── Dockerfile
├── app.py
├── docker-compose.yml
├── requirements.txt
└── nginx/
    └── default.conf
```

## 5.1 Flask Application

### `app.py`

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from the Flask backend!"


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### `requirements.txt`

```text
Flask
```

## 5.2 Backend Dockerfile

### `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

## 5.3 Nginx Reverse Proxy Configuration

### `nginx/default.conf`

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

The Nginx container uses the Compose service name `backend` to reach the Flask container.

## 5.4 Docker Compose Configuration

### `docker-compose.yml`

```yaml
services:
  backend:
    build: .
    container_name: compose-backend
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: compose-nginx
    ports:
      - "8080:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - backend
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## 5.5 Start the Application

From `05-compose`:

```bash
docker.compose up -d
```

This builds the Flask image and starts both services.

Check the services:

```bash
docker.compose ps
```

Expected services:

```text
compose-backend
compose-nginx
```

## 5.6 Test Through Nginx

Test the root endpoint:

```bash
curl http://localhost:8080
```

Expected:

```text
Hello from the Flask backend!
```

Test the health endpoint:

```bash
curl http://localhost:8080/health
```

Expected:

```text
OK
```

The request flow is:

```text
Client
  |
  v
Nginx :8080
  |
  v
Flask backend :5000
```

## 5.7 View Compose Logs

```bash
docker.compose logs
```

The logs should show:

* Flask starting on port `5000`
* Nginx starting successfully
* HTTP requests returning `200`
* Communication between Nginx and Flask

## 5.8 View Running Services

```bash
docker.compose ps
```

---

# Environment Variables

## MySQL Checkpoint

The MySQL container uses:

```text
MYSQL_ROOT_PASSWORD=rootpass
MYSQL_DATABASE=checkpointdb
```

These variables are used during MySQL initialization.

> For real-world applications, secrets should not be committed to source control. Use environment files, Docker secrets, or a cloud secrets manager.

---

# Docker Images Used

Official images used during this checkpoint:

```text
nginx:latest
nginx:alpine
python:3.12-slim
mysql:8.0
```

Custom images created:

```text
my-python-app:v1
05-compose-backend:latest
```

---

# Directory Structure

Final checkpoint structure:

```text
Docker-Checkpoint/
├── README.md
├── 02-dockerfile/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── 04-networking/
│   └── app.py
└── 05-compose/
    ├── Dockerfile
    ├── app.py
    ├── docker-compose.yml
    ├── requirements.txt
    └── nginx/
        └── default.conf
```

---

# Reproducing the Checkpoint

To reproduce the checkpoint from scratch:

1. Install Docker.
2. Pull the required official images.
3. Follow the Docker CLI exercises.
4. Build the custom Python image.
5. Create the MySQL volume.
6. Run the MySQL persistence test.
7. Create the `internal-net` network.
8. Run the container networking tests.
9. Enter `05-compose`.
10. Build and start the Flask + Nginx application:

```bash
docker.compose up -d
```

11. Verify:

```bash
docker.compose ps
curl http://localhost:8080
curl http://localhost:8080/health
```

12. Inspect logs:

```bash
docker.compose logs
```

---

# Skills Demonstrated

* Docker CLI
* Docker images
* Dockerfiles
* Docker containers
* Docker volumes
* Persistent storage
* Container networking
* Docker DNS/service discovery
* Port mapping
* Flask
* Nginx
* Reverse proxy configuration
* Docker Compose
* Multi-container applications
* Container lifecycle management
* Image layer inspection
* Basic application troubleshooting

---

# Checkpoint Status

| Area                        | Status   |
| --------------------------- | -------- |
| Docker Basics & CLI         | Complete |
| Docker Images & Dockerfiles | Complete |
| Docker Volumes & Storage    | Complete |
| Docker Networking           | Complete |
| Docker Compose              | Complete |

**Checkpoint completed successfully.**

