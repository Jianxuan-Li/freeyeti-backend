# Backend of freeyeti.net

## Development

### commands

* Requirement: Docker installed
* `./dev up` to start the container
* in the container run `poetry install` to install dependencies (just for first time)
* in the container run `./dev run` to start the backend server
* in the container run `./dev test` to run the tests
* exit the container with `exit`, then use `./dev down` to stop and remove the container

### .env.local

```bash
SECRET_KEY = "A_Tiger_app_2023"
```

### Dev server

* api is available at `http://localhost:8000/api/`
* wagtail admin is available at `http://localhost:8000/admin/`

## Deployment

- ingressroute is configured to route traffic to the backend service
- the url is `https://freeyeti.net/backend/`