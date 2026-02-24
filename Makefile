.PHONY: proto-go proto-python proto clean init tidy

proto: proto-go proto-python tidy

proto-go:
	@echo "Generating Go gRPC code..."
	python -c "import os; os.makedirs('action-service/pb', exist_ok=True)"
	protoc -I=proto --go_out=action-service/pb --go_opt=paths=source_relative --go-grpc_out=action-service/pb --go-grpc_opt=paths=source_relative tracker.proto

proto-python:
	@echo "Generating Python gRPC code for movement-service..."
	python -c "import os; os.makedirs('movement-service/pb', exist_ok=True)"
	python -m grpc_tools.protoc -I=proto --python_out=movement-service/pb --grpc_python_out=movement-service/pb tracker.proto
	python -c "open('movement-service/pb/__init__.py', 'a').close()"
	
	@echo "Generating Python gRPC code for audio-service..."
	python -c "import os; os.makedirs('audio-service/pb', exist_ok=True)"
	python -m grpc_tools.protoc -I=proto --python_out=audio-service/pb --grpc_python_out=audio-service/pb tracker.proto
	python -c "open('audio-service/pb/__init__.py', 'a').close()"

init:
	@echo "Creating virtual environments..."
	python -m venv movement-service\venv
	python -m venv audio-service\venv

	@echo "Updating Python tools..."
	movement-service\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
	audio-service\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
	
	@echo "Installing movement-service dependencies..."
	movement-service\venv\Scripts\python.exe -m pip install -r movement-service\requirements.txt
	
	@echo "Installing audio-service dependencies..."
	audio-service\venv\Scripts\python.exe -m pip install -r audio-service\requirements.txt
	
	@echo "Initializing Go module..."
	cd action-service && go mod tidy

tidy:
	@echo "Stripping unused Go dependencies and formatting code..."
	cd action-service && go mod tidy

clean:
	-rmdir /s /q action-service\pb
	-rmdir /s /q movement-service\pb
	-rmdir /s /q audio-service\pb