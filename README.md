# hitta-skyddsrum-services [![codecov](https://codecov.io/gh/hitta-skyddsrum/services/branch/master/graph/badge.svg)](https://codecov.io/gh/hitta-skyddsrum/services)


## Development
```
docker-compose up -d
docker-compose exec sandbox zsh
```

### Populate database
```
python -m HittaSkyddsrum.tests.db_populate HittaSkyddsrum/tests/*.gz
```

### Measure response time
```
./measure_response.sh "http://localhost:5000/api/v2/shelters/?lat=59.3524&long=18.0888" 200
```

## Deploy to production
Push to master and let  Travis do the rest.
