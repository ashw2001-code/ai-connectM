.PHONY: help setup clean

PYTHON = .venv/Scripts/python.exe
export PYTHONPATH = src

# Get all arguments after the target name
ARGS := $(filter-out $(firstword $(MAKECMDGOALS)),$(MAKECMDGOALS))

# Extract positional arguments
ARG1 := $(word 1,$(ARGS))
ARG2 := $(word 2,$(ARGS))
ARG3 := $(word 3,$(ARGS))
ARG4 := $(word 4,$(ARGS))

# Set defaults
N := $(if $(ARG1),$(ARG1),6)
M := $(if $(ARG2),$(ARG2),4)
H := $(if $(ARG3),$(ARG3),0)

# Prevent "No rule to make target" errors for numeric arguments
%:
	@:

help:
	@echo "Connect M Game - Available Commands:"
	@echo ""
	@echo "  make setup              - Set up the virtual environment"
	@echo "  make clean              - Clear Python cache and compiled files"
	@echo "  make help               - Show this help message"
	@echo ""
	@echo "PLAY INTERACTIVE GAME:"
	@echo "  make run [N] [M] [H]    - Play game (default: 6x6 Connect 4, human first)"
	@echo ""
	@echo "EXAMPLES:"
	@echo "  make run 6 4 0          - Play 6x6 Connect 4 (you first)"
	@echo "  make run 6 4 1          - Play 6x6 Connect 4 (AI first)"
	@echo "  make run 7 5 0          - Play 7x7 Connect 5 (you first)"
	@echo "  make run 8 4 1          - Play 8x8 Connect 4 (AI first)"

setup:
	@echo "Setting up virtual environment..."
	@call .venv\Scripts\activate.bat

clean:
	@echo "Clearing Python cache..."
	@powershell -Command "Get-ChildItem -Path . -Filter '__pycache__' -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; Get-ChildItem -Path . -Filter '*.pyc' -Recurse -Force | Remove-Item -Force -ErrorAction SilentlyContinue; Write-Host 'Cache cleared'"

run:
	@echo "Starting Connect M game ($(N)x$(N) Connect $(M), H=$(H))..."
	@$(PYTHON) -m my_package.main $(N) $(M) $(H)
