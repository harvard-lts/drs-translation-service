# drs-translation-service

[![Build Status](https://github.com/harvard-lts/drs-translation-service/actions/workflows/main.yml/badge.svg)](https://github.com/harvard-lts/drs-translation-service/actions)

## Local setup
    
1. Make a copy of the env-template.txt to .env and modify the user and password variables.

2. Put a copy of the [necessary version of Batch Builder](https://drive.google.com/drive/u/3/folders/0Bz4J5tiwltUzYzdTcGl3NC10bFk?resourcekey=0-mnguV0s8lW60H4VaVXoQKg) under the batch_builder_client directory.

3. In batch_builder_client/BatchBuilder_version/conf/bb.properties.dev, set the two values below:
ignoreinvalids=true
mods_hollis_url=http\://idtest.lib.harvard.edu:9020/rest/mods/hollis/

4. Start the container
    
```
docker-compose -f docker-compose-local.yml up -d --build --force-recreate
```

5. Local Healthcheck: https://localhost:10581/healthcheck

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
