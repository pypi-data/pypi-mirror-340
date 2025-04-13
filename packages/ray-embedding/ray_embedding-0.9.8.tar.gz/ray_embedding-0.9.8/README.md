# ray-embedding

A tool for deploying SentenceTransformers models to a ray cluster.

### Supports the following backends

- pytorch-gpu
- pytorch-cpu

### Planned:
- onnx-gpu
- onnx-cpu
- openvino-cpu
- fastembed-onnx-cpu
 
- spot instances
- grpc

### To build:
- python -m build
- twine upload dist/*

