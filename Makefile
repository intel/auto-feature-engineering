DOCKER_IMAGE_NAME ?= autofe_pyrecdp
DOCKER_NETWORK_NAME = autofe_workflow

autofe-local-workflow:
	@WORKSPACE=${workspace} \
	 DOCKER_IMAGE_NAME=${DOCKER_IMAGE_NAME} \
 	 docker compose up autofe-local-mode --build

autofe-EDA-UI:
	@WORKSPACE=${workspace} \
	 DOCKER_IMAGE_NAME=${DOCKER_IMAGE_NAME} \
 	 docker compose up autofe-EDA-UI --build

autofe-notebook-UI:
	@WORKSPACE=${workspace} \
	 DOCKER_IMAGE_NAME=${DOCKER_IMAGE_NAME} \
 	 docker compose up autofe-notebook-UI --build

autofe-dev:
	@WORKSPACE=${workspace} \
	 DOCKER_IMAGE_NAME=pyrecdp_ubuntu \
 	 docker compose up autofe-notebook-dev --build

clean: 
	docker network rm ${DOCKER_NETWORK_NAME}
	docker compose down