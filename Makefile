IMAGE_TAG_LATEST:=$(IMAGE_TAG_BASE):latest

DOCKERFILE = ./$(APP)/Dockerfile

DOCKER_RUN = docker run -p 80:80 --net=host -it --rm

# available APP options
APP_PARAM = telegram emailer password_editor auth_server

check-app-param:
ifndef APP
	$(error APP variable must be specified: [${APP_PARAM}])
endif

check-app: check-app-param
ifeq ($(filter $(APP),$(APP_PARAM)),)
	$(error "$(APP)" does not exist in [$(APP_PARAM)])
endif

check-auth:
	@[ -e $(HOME)/.docker/config.json ] && grep registry.yandex.net $(HOME)/.docker/config.json >/dev/null || ( \
		echo "==== No authorization, see https://wiki.yandex-team.ru/qloud/docker-registry/#cli ===="; \
		exit 255; \
	)

build: check-app
	docker build \
		-t $(IMAGE_TAG_LATEST) \
		-f $(DOCKERFILE) .

run: check-app
	$(DOCKER_RUN) $(IMAGE_TAG_LATEST)

push: check-app
	docker push $(IMAGE_TAG_LATEST)
