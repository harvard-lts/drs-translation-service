# drs-translation-service

## Local setup
    
1. Make a copy of the env-template.txt to .env and modify the user and password variables.

2. Start the container
    
```
docker-compose -f docker-compose-local.yml up -d --build --force-recreate
```

3. Local Healthcheck: https://localhost:10581/healthcheck

## Testing
Note, testing uses its own queues so they will not interfere with the queues used by the actual program.

1. Start the container up as described in the <b>Local Setup</b> instructions.

2. Exec into the container:

```
docker exec -it mqutils bash
```

3. Run the tests

```
pytest
```



