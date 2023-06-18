# KTH tasks

This repository contains my solutions to the challenges for interview.

*   **src** Contains the cli app
*   **documentation** Contatins the app documentation in mdbook format + 2nd challenge


# Running it all with docker

## Build and run

For the sake of simplicity i prepared Dockerfile(s) to let you test everything live. You need to run the following commands to start:

## Create network

    docker network create testNetwork

## Build images

Ansible **server**:

    docker build . -t kth_ansible_server -f .\docker\ansible_server\Dockerfile

**Client**:

    docker build . -t kth_client -f .\docker\debian_client\Dockerfile 


## Boot
Launch the **server** with the following command

    docker run --network testNetwork -t -i kth_ansible_server /bin/sh

and in the separate terminal/tab run the following to start the **client**.

    docker run --network testNetwork --name debian -t -i kth_client /bin/bash


## Start

First we need to prepare the client by restarting it's ssh service.

     service ssh restart

On the server do the following:

* generate key for login (ssh-keygen -t rsa)
* copy it to the root home directory of client (scp /root/.ssh/id_rsa.pub root@debian:/root/.ssh/authorized_keys). Password is "**Docker!**"

After all the steps done, we can run the tests with the following:

    python3 test_main.py

And to run cli app, run the following.

    python3 main.py debian
