# hitta-skyddsrum-services

## Development
```
docker build --build-arg USER=$USER -t hitta-skyddsrum-services .
docker run -v $PWD:/usr/src/app -u $(id -u) -dit hitta-skyddsrum-services
docker exec -it c8e /bin/sh

```
