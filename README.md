# ansible-scripts

Ansible installation Playbooks for provisioning VDI images for Eng. Faster Team.

# Quickstart

1. Install ansible (version 2.4+);
2. Clone this repository;
3. Create a new `.inventory` file or add the connection parameters to `base.inventory` in the project's `inventories` directory (see [here](#example-of-inventory-file));
4. Create the OS specific playbooks, if they do not exist. Check how to do it [here](#os-specific-playbooks).
4. Execute `ansible-playbook -i inventories/base.inventory -e HOSTS=local playbooks/base.yml` or use the `.inventory` file you created. Use the appropriate value
in the `HOSTS` variable to select the intended host definition.

## Example of inventory file

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


## OS Specific Playbooks

For each OS name and major distribution, there are three optional files that may be created:

* {os-name}\[-major-version\]-pre-tasks.yml

* {os-name}\[-major-version\]-packages.yml

* {os-name}\[-major-version\]-post-tasks.yml

Both the `os-version` and `major-version` are printed at the begining of `base.yml` play. Check if the required files exist in the `playbooks` directory.
If they don't exist, they will be skipped as no one is individually required. The major version of the file is optional. Therefore, both 
`Ubuntu-18.04-packages.yml` and `Ubuntu-packages.yml` are valid package list files. The former takes precedence on the later. 

`*-pre-tasks.yml` provides a list of tasks that must run at the begining of the play and `*-post-tasks.yml` lists define the tasks that must run at the end. They
may include every structure allowed in Playbook tasks. `*-packages.yml` is a list of packages available on the distro repository. The name of the packages may
be different depending on the distro. 
