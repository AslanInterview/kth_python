ssh-keygen -t rsa
scp /root/.ssh/id_rsa.pub root@debian:/root/.ssh/authorized_keys
