podman build --platform linux/amd64 --layers -t unisa-be:manifest-amd64 .

if [[ $(uname -p) == 'arm' ]]; then
    podman build --platform linux/arm64 --layers -t unisa-be:manifest-arm64 .
fi

podman rm -f unisa    

podman run -p 8000:8000 --name unisa localhost/unisa-be:manifest-amd64