__all__ = 'Task_runner'

import atexit
import os
from typing import List
import itertools

from ansible import context
from ansible.cli import CLI
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager

TMP_HOSTS = '.hosts.tmp'



class Task_Runner:
    """Executes the playbooks. Accepts the following params:

    Args:
        playbooks: the playbook/playbooks to run
        instances: list of hosts to use instead of specifying them in inventory
        inventories: your inventory file/files.
        (There must be "playbooks" and at least "inventoires" or "instances" param to make everything work)

    Optional args:
        remote_user: username, used for connecting to the remote hosts
        remote_pass: password for remote_user. Use None if it doesn't have one
        connection: specifies the type of connection used for contatcing with the remote host
        private_key_file: private key, used for connections
        become: whether we should escalate our privileges or not

    """

    def __init__(self, playbooks: List[str], instances: List[str] = None, inventories: List[str] = None,
                 remote_user=None, remote_pass=None, connection="ssh", become=True):
        # Adapted from here: https://stackoverflow.com/a/57501942

        # check if recieved params are valid
        if not isinstance(playbooks, list):
            raise ValueError("Playbooks must be specifed")

        if not isinstance(instances, list) and not isinstance(inventories, list):
            raise ValueError("instances or/and inventories must be specified and be list/lists")

        if isinstance(instances, list) and not inventories != None and isinstance(inventories, list):
            raise ValueError("inventories must be list")
        elif isinstance(inventories, list) and instances != None and not isinstance(instances, list):
            raise ValueError("instances must be list")

        sources = []

        # create a temporary file for storing supplied hosts
        if instances != None and len(instances):
            with open(TMP_HOSTS, "w") as f:
                for instance in instances:
                    f.write(f"{instance}\n")
            atexit.register(lambda: os.remove(TMP_HOSTS))
            sources = [TMP_HOSTS]

        if inventories != None and len(inventories):
            sources = list(itertools.chain(sources, inventories))

        loader = DataLoader()
        context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection=connection,
                                        module_path=None, forks=100, remote_user=remote_user, remote_pass=remote_pass, private_key_file=None,
                                        ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=become,
                                        become_method="sudo", become_user="root", verbosity=False, check=False, start_at_task=None)
        print(sources)
        inventory = InventoryManager(loader=loader, sources=sources)

        variable_manager = VariableManager(
            loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))

        self.__pbex = PlaybookExecutor(playbooks=playbooks, inventory=inventory,
                                       variable_manager=variable_manager, loader=loader, passwords={})

    def run_tasks(self):
        """Runs the playbook and return 0 if successful"""
        return self.__pbex.run()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print(f"Usage {sys.argv[0]}: instance_name_or_ip instance_name_or_ip ... instance_name_or_ip")
        exit(-1)

    instances = sys.argv[1::]
    # running the playbook.yml on all the hosts supplied via command line
    Task_Runner(playbooks=["playbook.yml"], instances=instances, remote_user="root", remote_pass="Docker!").run_tasks()
