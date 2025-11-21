.PHONY: test lint install

# Delegate commands to the trips microservice
test:
	$(MAKE) -C trips test

lint:
	$(MAKE) -C trips lint

install:
	pip install -r trips/requirements.txt
