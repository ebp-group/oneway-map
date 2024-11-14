Follow guide: https://fly.io/docs/app-guides/minio/

Create volume with at least 50GB size.

## Zugriff via Webinterface

Proxy für Port 9001 laufen lassen:

```
flyctl proxy 8080:9001
```

Anschliessend Zugriff via http://localhost:8080/
