# Wiki

## Installation Guide

### 0. Install docker

Ensure Docker is installed on your system. For installation instructions, please visit [the official guide](https://docs.docker.com/engine/install/ubuntu/).

### 1. Prepare the docker image

DevBench offers two versions of Docker images: the base version and the complete version. Select the appropriate version based on your requirements:

|   Tag    | dep. for DevBench utilities and baseline system | dep. for Python repos | dep. for C++/Java/JS repos |
| :------: | :-------------------------------------------------: | :-------------------: | :------------------------: |
|   [base](./docker/base/)   |                       ✅                            |          ❌           |     ❌                     |
| [complete](./docker/complete/) |                       ✅                            |          ✅           |     ❌                     |

- **Base Version:** Ideal for evaluating environment setup tasks, this version provides a clean and initial setting with essential tools. It is tailored for scenarios where a clean, minimal environment is crucial. It includes:
  - Core dependencies for DevBench utilities and the baseline system.
  - Key utilities such as compilers (gcc, g++ 11), GoogleTest, Java 14, Python 3.11, node.js, cmake, and MiniConda.
  - Specific third-party tools for C++, JS, and Java repositories, like Redis for Java redis-cache and Sqlite for the C++ database management repository.
  - Essential packages to operate the baseline agent system efficiently.

- **Complete Version:** Recommended for implementation and testing tasks, it encompasses everything in the base version plus:
  - Comprehensive dependencies for all Python repositories, facilitating a seamless development experience without the hassle of manual dependency management.

**Note:** Our evaluation of environment setup primarily targets Python and JavaScript projects. We've chosen to concentrate on these languages because they have well-established tools for package management, unlike C++. C++ lacks a universally accepted package manager, which makes standardized environment setup challenging. In contrast, Java projects often incorporate their own comprehensive build and package management systems, commonly utilizing scripts like Gradle. Therefore, our environment setup process is less relevant to Java projects. Instead, for Java, we integrate the environment setup evaluation with the implementation phase. During this combined phase, the model or agent is required to execute a complete Gradle script, which includes all necessary dependency listings and build instructions.

This structured approach ensures that developers can choose the most suitable environment, enhancing their efficiency and the overall development workflow.

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