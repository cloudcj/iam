# Docker Compose Setup for Redis (In-Memory Only)

This documentation describes how to run a **Redis server** using Docker Compose for your Django inventory system, specifically for JWT token blacklisting. This setup uses **in-memory storage only**, meaning all data will be lost if the container stops.

---

## docker-compose.yml

```yaml
services:
  redis:
    image: redis:8.2.1               # latest Redis version
    container_name: redis_blacklist
    ports:
      - "6379:6379"                 # expose Redis port to host
    restart: always
    command: ["redis-server", "--save", "", "--appendonly", "no"]  # disables persistence
```

---

## How it Works

* **Service name:** `redis`
  Can be referenced in Django via `REDIS_HOST=redis` when using Docker networking.

* **Port:** 6379
  Map container port to host port for local testing.

* **Restart policy:**
  `always` automatically restarts the container if it crashes or the Docker daemon restarts.

* **In-memory only:**
  Using `--save ""` and `--appendonly no` disables persistence.
  ⚠️ All keys will be lost if the container is stopped or restarted.

---

## Usage

### 1. Start Redis

```bash
docker-compose up -d redis
```

* `-d` runs the container in detached mode.

### 2. Shutdown Redis

```bash
docker-compose down
```

* Stops and removes containers, networks, and default volumes created by `up`.

### 3. Restart Redis

```bash
docker-compose restart redis
```

* Restarts the Redis container without removing it.

### 4. Check Running Containers

```bash
docker ps
```

* You should see `redis_blacklist` running on port 6379.

### 5. Access Redis CLI

```bash
docker exec -it redis_blacklist redis-cli
```

### 6. Test Connectivity

```bash
PING
# Should return: PONG
```

### 7. Inspect Keys

```bash
KEYS *
# Lists all keys currently in Redis
```

### 8. Flush Database (Optional)

```bash
FLUSHALL
# Clears all keys in memory
```

---

## Django Integration

Add the following to your `.env` file:

```
REDIS_HOST=localhost          # or 'redis' if in Docker network
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=               # leave blank if no password
```

---

## JWT Blacklisting Notes

1. **LogoutView:**

   * Blacklist refresh tokens in Redis with `ttl = token.exp - now`.
   * Optionally, blacklist access tokens if you want immediate invalidation.

2. **CustomAuthentication:**

   * Check `cache.get(f"blacklist:{jti}")` for access tokens.
   * Reject requests if found.

3. **TokenRefreshView:**

   * Before issuing a new access token, check if the refresh token is blacklisted.

---

### Next Steps

1. Run Redis with `docker-compose up -d redis`.
2. Verify connection in Django shell:

```python
from django.core.cache import cache
cache.set("test-key", "ok", timeout=60)
print(cache.get("test-key"))  # Should print: ok
```
