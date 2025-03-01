install:
	@echo "Installing AutoLinker libraries..."
	@pip install -r requirements.txt

run:
	@echo "Running AutoLinker..."
	@python main.py
