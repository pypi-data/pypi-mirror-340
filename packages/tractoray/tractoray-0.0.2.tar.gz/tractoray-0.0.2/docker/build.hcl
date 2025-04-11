target "jammy_python_sys" {
  platforms = ["linux/amd64"]
  dockerfile-inline = <<EOT
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    python3 -m pip install --upgrade pip
EOT
}

target "tests" {
  platforms = ["linux/amd64"]
  contexts = {
    base_image = "target:jammy_python_sys"
  }
  context = "${PROJECT_ROOT}"
  tags = [
    "${DOCKER_REPO}/tractoray/tests:${DOCKER_TAG}"
  ]
  dockerfile-inline = <<EOT
FROM base_image

RUN apt install net-tools telnet --yes
RUN apt install wget --yes
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN apt-get update
RUN apt-get -y install cuda-toolkit-12-4 --yes
ENV PATH=/usr/local/cuda-12.4/bin:$PATH
ENV CUDA_HOME=/usr/local/cuda-12.4
RUN pip3 install --upgrade pip setuptools wheel

RUN apt install socat --yes

RUN pip3 install poetry poetry-plugin-export

RUN mkdir /src
COPY ./pyproject.toml /src/pyproject.toml
COPY ./poetry.lock /src/poetry.lock

RUN cd /src && poetry export --with=tests --without-hashes --format=requirements.txt > requirements.txt
RUN cd /src && pip install -r requirements.txt
EOT
}

target "jupyter" {
  platforms = ["linux/amd64"]
  contexts = {
    base_image = "target:jammy_python_sys"
  }
  context = "${PROJECT_ROOT}"
  tags = [
    "${DOCKER_REPO}/tractoray/jupyter:${DOCKER_TAG}"
  ]
  dockerfile-inline = <<EOT
FROM base_image

RUN apt install net-tools telnet --yes
RUN apt install wget --yes
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN apt-get update
RUN apt-get -y install cuda-toolkit-12-4 --yes
ENV PATH=/usr/local/cuda-12.4/bin:$PATH
ENV CUDA_HOME=/usr/local/cuda-12.4
RUN pip3 install --upgrade pip setuptools wheel

RUN apt install socat --yes

RUN mkdir /src
COPY ./ /src

RUN poetry config virtualenvs.create false && cd /src && poetry install --with=tests
EOT
}

target "synthlab" {
  platforms = ["linux/amd64"]
  contexts = {
  }
  context = "${PROJECT_ROOT}"
  tags = [
    "${DOCKER_REPO}/tractoray/jupyter-synthlab:${DOCKER_TAG}"
  ]
  dockerfile-inline = <<EOT
FROM cr.eu-north1.nebius.cloud/e00faee7vas5hpsh3s/synthlabstest.azurecr.io/verl/verl-ray-fsdp:v1

RUN rm -rf /src
RUN mkdir /src
COPY ./ /src

RUN poetry config virtualenvs.create false && cd /src && poetry install --with=tests
EOT
}
