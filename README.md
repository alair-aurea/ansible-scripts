# ansible-scripts

Ansible installation Playbooks for provisioning VDI images for Eng. Faster Team.

# Quickstart

1. Install ansible (version 2.4+);
2. Clone the repository;
3. Create an `.inventory` file in the project's root directory to define the connection parameters (see bellow);
4. Execute `ansible-playbook -i file.inventory base.yml`

## Example of inventory file for windows target machine

```
[vdi]
vbox_host ansible_ssh_host=192.168.56.101 vbox_host_alias=vbox_host

[local]
local_host ansible_ssh_host=127.0.0.1 local_host_alias=local_host

[all:vars]
ansible_connection=ssh 
ansible_ssh_user=root
ansible_ssh_pass=password
```

### Remarks

* The `ansible_ssh_pass` variable might be not necessary if connection to the target machine is secured by a SSH key.

* The base playbook (**base.yml**) perform the tasks defined for all hosts under the `[vdi]` tag of the inventory file.

* The `.gitignore` file excludes all `*.inventory` files from version control.
