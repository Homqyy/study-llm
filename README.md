# Study-LLM

OS: ubuntu22.04

GPU: [GeForce RTX 4080 Super](https://www.techpowerup.com/gpu-specs/geforce-rtx-4080-super.c4182)

Python: 3.10.12

## download model

### with huggingface-cli

1. Install the CLI tool:

    ```bash
    pip install -U huggingface_hub
    ```

2. Set the mirror URL for downloading:

    ```bash
    # Linux
    export HF_ENDPOINT=https://hf-mirror.com

    # Windows
    $env:
    ```

3. Download the model:

    ```bash
    huggingface-cli download --resume-download <model_name> --local-dir <save_path>
    ```

4. download datasets:

    ```bash
    huggingface-cli download --resume-download --repo-type dataset <dataset_name> --local-dir <save_path>
    ```

### with modelscope CLI

-

## running on docker

docker version: Docker Desktop and WSL

docker raw image: <https://hub.docker.com/r/nvidia/cuda>

docker image for China: `homqyy/cuda:12.6.3-runtime-ubuntu22.04-CN`
