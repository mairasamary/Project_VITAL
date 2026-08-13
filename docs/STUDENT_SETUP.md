# Project VITAL — Student Setup Guide

This guide prepares your computer to run the Project VITAL software-testing environment.

Project VITAL uses **OpenEMR** as the System Under Test (SUT). OpenEMR runs locally inside Docker containers, so you do not need to install PHP, MariaDB, or OpenEMR directly.

By the end of this setup, you should be able to open OpenEMR in your browser and log in to your own local instance.

---

## 1. What You Need

Before beginning, make sure you have:

- Windows, macOS, or Linux
- Internet access
- Git
- Docker and Docker Compose
- A modern web browser
- Terminal access
- Sufficient free disk space for Docker images and course data

You do **not** need prior Docker experience.

---

# Part I — Install Git

## 2. Check Whether Git Is Installed

Open Terminal on macOS/Linux or PowerShell/Git Bash on Windows:

```bash
git --version
```

You should see something similar to:

```text
git version 2.x.x
```

If `git` is not found, install Git, restart your terminal, and run the command again.

---

# Part II — Install and Start Docker

## 3. macOS

Install **Docker Desktop** from Docker's official website. Choose the version for Apple Silicon or Intel as appropriate.

To identify your Mac:

1. Select the Apple menu.
2. Choose **About This Mac**.
3. Look for **Chip** or **Processor**.

After installation:

1. Open **Applications**.
2. Open **Docker**.
3. Accept requested terms and permissions.
4. Wait for Docker Desktop to finish starting.

**Important:** Installing Docker Desktop is not enough. Docker Desktop must be running before `docker` commands will work.

## 4. Windows

Install **Docker Desktop for Windows** from Docker's official website.

Docker may ask you to enable or use **WSL 2**. Follow Docker Desktop's recommended configuration.

After installation:

1. Start Docker Desktop.
2. Wait until Docker reports that the engine is running.
3. Keep Docker Desktop running while working on Project VITAL.

## 5. Linux

Install Docker Desktop or Docker Engine using Docker's official instructions for your distribution. Also install the Docker Compose plugin.

Check the Docker service:

```bash
sudo systemctl status docker
```

If necessary:

```bash
sudo systemctl start docker
```

Depending on your configuration, you may initially need `sudo` for Docker commands.

---

# Part III — Verify Docker

## 6. Check Docker and Docker Compose

```bash
docker --version
docker compose version
```

Project VITAL uses Docker Compose v2:

```bash
docker compose
```

Do not use the older `docker-compose` command unless specifically instructed.

## 7. Verify That the Docker Engine Is Running

```bash
docker info
```

A successful response includes server information such as containers, images, server version, and storage information.

If you see:

```text
Cannot connect to the Docker daemon
```

Docker is installed but its engine is not running.

On macOS/Windows, open Docker Desktop and wait for it to finish starting. On Linux, check/start the Docker service. Then run `docker info` again.

## 8. Test Docker

```bash
docker run hello-world
```

A successful run displays a message indicating that Docker is working correctly.

If this fails, **do not proceed to OpenEMR**. Resolve the Docker installation first.

---

# Part IV — Download Project VITAL

## 9. Clone the Course Repository

Choose a location for course projects, then:

```bash
git clone https://github.com/mairasamary/Project_VITAL.git
cd Project_VITAL
```

Check the repository:

```bash
ls
```

You should see directories such as:

```text
assignments
data
docs
environment
instructor
rubrics
tests
```

Windows PowerShell users may use `dir`.

---

# Part V — Prepare OpenEMR

## 10. Enter the Environment Directory

```bash
cd environment
```

Check its contents:

```bash
ls -a
```

You should see:

```text
docker-compose.yml
.env.example
README.md
VERSION.md
setup.sh
reset.sh
status.sh
```

## 11. Create Your Local Configuration

### macOS/Linux

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

The `.env` file contains local settings such as ports, database credentials, and the OpenEMR administrator account.

**Do not commit `.env` to GitHub.** Project VITAL's `.gitignore` excludes it.

---

# Part VI — Download the OpenEMR Environment

## 12. Pull Docker Images

First confirm Docker is running:

```bash
docker info
```

Then:

```bash
docker compose pull
```

Docker downloads the pinned OpenEMR and MariaDB images. The first download may take several minutes.

---

# Part VII — Start OpenEMR

## 13. Start the Containers

```bash
docker compose up -d
```

The `-d` option runs the containers in the background.

Initial startup can take several minutes while MariaDB initializes and OpenEMR completes setup.

## 14. Check Status

```bash
docker compose ps
```

You should eventually see:

```text
vital-openemr-app
vital-openemr-db
```

If a container shows `Exited`, `Restarting`, or `Unhealthy`, use the troubleshooting steps below.

## 15. View Startup Logs

```bash
docker compose logs -f openemr
```

Press **Ctrl+C** to stop watching the logs. This does not stop OpenEMR.

---

# Part VIII — Open OpenEMR

## 16. Open the Application

Use:

```text
http://localhost:8080
```

HTTPS may also be available at:

```text
https://localhost:8443
```

A local HTTPS certificate may cause a browser warning. Unless instructed otherwise, use `http://localhost:8080`.

## 17. Log In

Default Project VITAL credentials:

```text
Username: admin
Password: vital-admin
```

Your instructor may provide different credentials.

---

# Part IX — Verify the Complete Setup

## 18. Setup Checklist

Before Assignment 1, verify:

- [ ] `git --version` works
- [ ] `docker --version` works
- [ ] `docker compose version` works
- [ ] `docker info` works
- [ ] `docker run hello-world` works
- [ ] Project VITAL has been cloned
- [ ] `environment/.env` exists
- [ ] `docker compose pull` completes
- [ ] `docker compose up -d` completes
- [ ] `docker compose ps` shows OpenEMR and MariaDB running
- [ ] `http://localhost:8080` opens
- [ ] You can log in to OpenEMR

Do not begin Assignment 1 until all items are working.

---

# Part X — Everyday Use

## 19. Starting Project VITAL Later

Start Docker Desktop first on macOS/Windows, then:

```bash
cd Project_VITAL/environment
docker compose start
```

Open `http://localhost:8080`.

## 20. Stopping OpenEMR

```bash
docker compose stop
```

Your database and changes remain available for the next session.

## 21. Checking Status

```bash
docker compose ps
```

On macOS/Linux you may also use:

```bash
./status.sh
```

---

# Part XI — Resetting OpenEMR

Testing sometimes requires returning to a known baseline.

### macOS/Linux

```bash
./reset.sh
```

Alternatively:

```bash
docker compose down -v
docker compose up -d
```

**Warning:** deleting Docker volumes removes patients, appointments, encounters, database modifications, and other local OpenEMR data.

Do not reset unless instructed or unless you understand that your current data will be deleted.

---

# Part XII — Common Problems

## Cannot connect to the Docker daemon

Example:

```text
Cannot connect to the Docker daemon at
unix:///Users/.../.docker/run/docker.sock.
Is the docker daemon running?
```

**Cause:** Docker is installed, but Docker Desktop/Engine is not running.

**macOS/Windows:** start Docker Desktop, wait for it to report that Docker is running, then:

```bash
docker info
```

**Linux:**

```bash
sudo systemctl start docker
```

## `docker: command not found`

Docker is not installed or the terminal cannot find it. Install Docker and restart the terminal.

## `docker compose` does not work

Check:

```bash
docker compose version
```

Project VITAL requires Docker Compose v2.

## Port 8080 is already in use

Edit `environment/.env` and change:

```text
OPENEMR_HTTP_PORT=8080
```

to, for example:

```text
OPENEMR_HTTP_PORT=8081
```

Restart:

```bash
docker compose down
docker compose up -d
```

Then open `http://localhost:8081`.

## OpenEMR does not open immediately

Check:

```bash
docker compose ps
docker compose logs openemr
```

Initial startup may take several minutes.

## Something is badly broken

You can recreate the local environment:

```bash
docker compose down -v
docker compose up -d
```

Remember: this deletes your local database.

---

# Part XIII — Course Safety Rules

Project VITAL provides an isolated environment so software testing can be performed safely.

1. **Never enter real patient information.**
2. Use only synthetic course data.
3. Do not perform security testing against public OpenEMR websites, demos, or external servers.
4. SQL injection, load testing, denial-of-service experiments, and similar activities may target only the isolated environment authorized by your instructor.
5. Do not expose the OpenEMR Docker environment to the public Internet.
6. Do not commit passwords, `.env` files, tokens, or credentials to GitHub.
7. Do not upload course-generated healthcare-style datasets to external services unless explicitly authorized.

---

# You're Ready

When you can:

```text
Start Docker
        ↓
Start Project VITAL
        ↓
Open localhost:8080
        ↓
Log into OpenEMR
```

you have successfully completed the Project VITAL environment setup.

Your next step is **Assignment 1: System Understanding**.
