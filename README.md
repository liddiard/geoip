# GeoIP

Tiny Flask server to proxy [MaxMind GeoLite](https://dev.maxmind.com/geoip/geolocate-an-ip/web-services/) requests. Get the estimated city, country, and coordinates of a user's IP.

## Installation

1. [Sign up](https://www.maxmind.com/en/geolite2/signup) for a free GeoLite API key.
2. Once signed up, create a MaxMind license key.
3. Within the repo, run `cp .env.example .env`.
4. In the `.env` file, fill in the environment variables with your license key info.

Next, follow the instructions below to run the app.

### Docker (recommended)

1. Run `docker compose up`.

### Without Docker

1. [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/).
2. Run `uv sync`.
3. Run `uv run python app.py`.

## Usage

Once the app is running, make a request to http://localhost:5050 with a valid public IP address in the `X-Forwarded-For` header. For example:

```shell
curl --location 'localhost:5050' --header 'X-Forwarded-For: 75.219.240.157'
```

You should get a response like:

```json
{
  "city": "Brooklyn",
  "country_code": "US",
  "country_name": "United States",
  "ip": "75.219.240.157",
  "latitude": 40.6462,
  "longitude": -73.9559
}
```

If deploying on a public server behind a reverse proxy, ensure that you set the `X-Forwarded-For` header to pass along the requestor's IP address to the application. For example on Nginx:

```nginx
server {
    server_name geoip.harrisonliddiard.com;

    location / {
        proxy_pass http://localhost:5050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
