# app usage

The app syntax is simple. It saves all the hostnames/IPs provided via command line and executes the playbook named "playbook.yml" which must be located at the same directory as the cli app.

There is an already prepared example ansible role, 
located in folder named "roles" which can be executed by executing the playbook named **role_playbook.yml**.

Example:

    python3 main.py debian ubuntu 192.168.50.10

This example will run the playbook.yml for hosts named "debian", "ubuntu" and 192.168.50.10.

