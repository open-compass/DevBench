# Wiki

## Installation Guide

### 0. Install docker

Ensure Docker is installed on your system. For installation instructions, please visit [the official guide](https://docs.docker.com/engine/install/ubuntu/).

### 1. Prepare the docker image

DevBench offers two versions of Docker images: the base version and the complete version. Choose the one that fits your needs:

|   Tag    | dep. for DevBench utilities and baseline system | dep. for Python repos | dep. for C++/Java/JS repos |
| :------: | :-------------------------------------------------: | :-------------------: | :------------------------: |
|   [base](./docker/base/)   |                       ✅                            |          ❌           |     ❌                     |
| [complete](./docker/complete/) |                       ✅                            |          ✅           |     ❌                     |

- Base version: The base version contains the dependencies for the DevBench utilities and the baseline agent system. Utilities provided by the base version contains:
  - Compiler, testing, build and package management tools: gcc and g++ 11, GoogleTest, Java 14, Python 3.11, node.js, cmake and MiniConda.
  - C++, JS and Java repository-specific third-party tools, such as Redis for the Java redis-cache repository and Sqlite for the C++ database management repository.
  - Necessary packages to get the baseline agent system running.
- Complete version: In addition to all packages provided by the base version,
  - Complete dependencies for all Python repositories.

#### Option 1: Build from dockerfiles

- Base image:

```shell
cd docker/base
docker build -t $IMAGE_NAME:$VERSION .
```

- Complete image:

```shell
cd docker/complete
docker build -t $IMAGE_NAME:$VERSION .
```

#### Optional 2: Pull images from docker hub

Alternatively, you can pull the pre-built images from [docker hub](https://hub.docker.com/r/elyndendu/devbench).

- Base image.

```shell
docker pull elyndendu/devbench:base
```

- Complete image.

```shell
docker pull elyndendu/devbench:complete
```

### 2. Utilize nvidia GPUs in docker (optional)

To use nvidia GPUs within Docker, install the nvidia container toolkit by following these steps:

```shell
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```

### 3. Create the docker container

To create a container with nvidia GPU support:

```shell
docker run -it --gpus all --name $CONTAINER_NAME -e NVIDIA_DRIVER_CAPABILITIES=compute,utility -e NVIDIA_VISIBLE_DEVICES=all $IMAGE_NAME:$VERSION bash
```

For a standard setup without GPU support:

```shell
docker run -it --name $CONTAINER_NAME devbench:$VERSION bash
```

### 4. Clone our Devbench

```shell
git clone git@github.com:open-compass/DevBench.git
```

### 5. Run sanity checks

Run unit and acceptance tests for each repo as per the [instructions](./benchmark_data/README.md#dataset-introduction) in the `repo_config.json` in `repo_config.json` found in `benchmark_data`.

For example, for the repo `./benchmark_data/python/readtime`, a fragment of `repo_config.json` is shown as follows:

```json
{
    "unit_test_script": "pytest --cov=. --cov-report=json:unit_test_cov.json --json-report --json-report-file=unit_test_report.json unit_tests",
    "acceptance_test_script": "pytest --cov=. --cov-report=json:acceptance_test_cov.json --json-report --json-report-file=acceptance_test_report.json acceptance_tests",
}
```

If tests fail due to network issues, simply retry.