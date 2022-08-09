 python -m grpc_tools.protoc -I. --python_out=./ --grpc_python_out=./ .\test.
proto  
 

# demo3
单项流
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. demo.proto