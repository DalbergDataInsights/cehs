# Continuity of Essential Health Services

# Launching with docker-compose

## Bring the compose online

```bash
docker-compose up
```

## You may have to build or rebuild the container
```bash
docker build .
```

# Launching with docker

## Building a container
```bash
docker build -t viz .
```


## Launching a container
```bash
docker run --name viz-dev -it -p 8050:8050 -v /Users/denyssementsov/Documents/Projects/DDI/icohs/:/app/ viz bash
```