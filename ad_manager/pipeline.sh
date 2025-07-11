echo "Derrubando containers..."
docker compose down

echo "Subindo containers..."
docker compose up -d --build
echo "containers online!"