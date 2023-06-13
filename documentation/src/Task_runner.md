# Task_Runner


This class provides a simple, portable and convinient API for
seamless interaction with ansible for automation needs.

I have chosen to not use the subprocess library
because of the unnecessary costs of starting the python 
aplication over and over. It can be absoulutely inapropporiate
to spawn like 10+ python subprocesses at the same time,
conseuquantely wasting the valuable resourses.

## running the class

First, you need to import the module

    from main import Task_Runner


Then, you must to provide it with the following params:

* playbooks (required)
* instances (required/can be replaced with "inventories")
* inventories (required/can be replaced with "instances")

All this parameters **must be** lists with ***str*** elements inside.

- **playbooks.** Specifies playbooks to be executed.

- **instances.** List of hosts to run playbook on.

- **inventories.** List of ansible inventories

Also, the Task_Runner class supports the following optional parameters:

* **remote_user.**: username, used for connecting to the remote hosts

* **remote_pass.** password for remote_user. Use None if it doesn't have one

* **connection.** specifies the type of connection used for contatcing with the remote host

* **private_key_file.** private key, used for connections

* **become.** Determines, whether we should escalate our privileges on a target machine or not.


**Examples**:

**Running a playbook called "playbook.yml" and inventory "hosts"**:

    Task_Runner(playbooks=["playbook.yml"], inventories=["hosts"]).run_tasks()

**Running with the list of hosts instead of inventory file. 
This creates new inventory file with hosts line by line, so we supply the username as well**

    Task_Runner(playbooks=["playbook.yml"], instances=["debian"], remote_user="ansible").run_tasks()

**Running with custom instances list**

    Task_Runner(playbooks=["playbook.yml"], inventories=["hosts"], instances=["debian"], remote_user="ansible").run_tasks()
