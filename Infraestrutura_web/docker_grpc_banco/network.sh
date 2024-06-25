REDE_WEB="rede_web"

docker network create --driver bridge $REDE_WEB

echo "Redes Docker criadas com sucesso: "
docker network ls

echo "Redes configuradas com sucesso."

# Manter o container em execução
exec "$@"
