# ansible-scripts
...!...
Ansible installation Playbooks for provisioning VDI images for Eng. Faster Team.

# Quickstart

1. Install ansible (version 2.4+);
2. Clone this repository;
3. Create a new `.inventory` file or add the connection parameters to `base.inventory` in the project's `inventories` directory (see bellow);
4. Execute `ansible-playbook -i inventories/base.inventory -e HOSTS=local playbooks/base.yml` or use the `.inventory` file you created. Use the appropriate value
in the `HOSTS` variable to select the intended host definition.

## Example of inventory file for linux local target machine

```
[local]
local_host ansible_ssh_host=127.0.0.1 local_host_alias=local_host

[local:vars]
ansible_ssh_user=root
ansible_ssh_pass=password
ansible_connection=ssh 
```

There are two entries for each target machine. First, the host (target) connection definitions, like its IP address. Then, the variables, which
define how to setup the connection. If the connection is secured by a SSH key to connect the variable `ansible_ssh_pass` is not required.


