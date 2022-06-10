docker stop mainmapserver
docker stop secondmapserver
docker stop mongo
yes | docker container prune
docker volume rm mongo_db-volume
docker compose build
docker compose up