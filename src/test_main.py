import os
import unittest
from pprint import pprint

import paramiko

from main import Task_Runner

HOSTNAME = "debian"
USERNAME = "root"
PASSWORD = "Docker!"

TMP_PLAYBOOK = "temp_playbook.tmp"

TMP_FILE = "unittest.tmp"

PLAYBOOK_COPY_TO_REMOTE =f"""---
- name: Install docker
  gather_facts: No
  hosts: all
  tasks:
    - name: move hello_world.c to /tmp
      copy:
        src: {TMP_FILE}
        dest: /tmp/{TMP_FILE}
"""

class TestMain(unittest.TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super(TestMain, self).__init__(*args, **kwargs)
        self.attribute = "new"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=HOSTNAME, port=22,
                         username=USERNAME, password=PASSWORD)
        # will be used for retrieving list of files from the "tmp" folder
        self.ftp = self.ssh.open_sftp()
        self.tmp_folder_contents = self.ftp.listdir("/tmp")
        try: self.ftp.remove(f"/tmp/{TMP_FILE}")
        except: ...

    def __make_tmp_playbook(self, content: str):
        with open(TMP_PLAYBOOK, "w") as f:
            f.write(content)

    def test_run_sample_playbook(self):
        '''Creates a temporary file and copies it to remote machine via ansible'''
        with open(TMP_FILE, "w") as f:  f.write("sample text")
        self.__make_tmp_playbook(PLAYBOOK_COPY_TO_REMOTE)
        Task_Runner(playbooks=[TMP_PLAYBOOK], instances=["debian"], remote_user=USERNAME, remote_pass=PASSWORD, become=False).run_tasks()
        tmp_folder_contents = self.ftp.listdir("/tmp")
        self.assertTrue(TMP_FILE in tmp_folder_contents)

    def test_throw_invalid_arg(self):
        '''Checks whether the expected ValueError occurs when needed'''
        with self.assertRaises(ValueError):
            Task_Runner(playbooks=["playbook.yml"], instances="debian")
        with self.assertRaises(ValueError):
            Task_Runner(playbooks="playbook.yml", instances=None)
        with self.assertRaises(ValueError):
            Task_Runner(playbooks="playbook.yml", instances=["debian"], inventories="hosts")

        Task_Runner(playbooks="playbook.yml", instances=["debian"], inventories="hosts")


    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:    os.remove(TMP_PLAYBOOK)
        except: ...

if __name__ == "__main__":
    unittest.main()
    


