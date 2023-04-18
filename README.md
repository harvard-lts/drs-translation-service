# drs-translation-service

[![Build Status](https://github.com/harvard-lts/drs-translation-service/actions/workflows/main.yml/badge.svg)](https://github.com/harvard-lts/drs-translation-service/actions)

## Local setup
    
1. Make a copy of the env-template.txt to .env and modify the user and password variables.

2. Put a copy of the necessary version of Batch Builder under the batch_builder_client directory.

3. Start the container
    
```
docker-compose -f docker-compose-local.yml up -d --build --force-recreate
```

3. Local Healthcheck: https://localhost:10581/healthcheck

## Testing
Note, testing uses its own queues so they will not interfere with the queues used by the actual program.

1. Start the container up as described in the <b>Local Setup</b> instructions.

2. Exec into the container:

```
docker exec -it dts bash
```

3. Run the tests

```
pytest
```



