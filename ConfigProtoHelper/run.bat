protoc -I ../Config/ --csharp_out=../Config/ ../Config/Data.proto
protoc -I ../Config/ --python_out=./ ../Config/Data.proto
protoc -I ../Config/ --python_out=../Test/ ../Config/Data.proto
pause