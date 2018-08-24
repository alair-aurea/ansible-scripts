# ansible-scripts

Ansible installation Playbooks for provisioning VDI images for Eng. Faster Team.

# Quickstart

1. Install ansible (version 2.4+);
2. Clone this repository;
3. Create a new `.inventory` file or add the connection parameters to `base.inventory` in the project's `inventories` directory (see [here](#example-of-inventory-file));
4. Create the OS specific playbooks, if they do not exist. Check how to do it [here](#os-specific-playbooks).
4. Execute `ansible-playbook -i inventories/base.inventory -e HOSTS=aws-vdi playbooks/base.yml` or use the `.inventory` file you created. Use the appropriate value
in the `HOSTS` variable to select the intended host definition.

## Example of inventory file

```
[ubuntu-vdi]
ubuntu_vdi ansible_ssh_host=vm-00017a95.vdi-vm.devfactory.com ubuntu_vdi_alias=ubuntu_vdi

[ubuntu-vdi:vars]
ansible_connection=ssh 
ansible_ssh_user=ubuntu
ansible_ssh_private_key_file="{{inventory_dir}}/ubuntu-vdi.pem"
ansible_python_interpreter=/usr/bin/python3

[windows-vdi]
windows_vdi ansible_ssh_host=vm-00017a9f.vdi-vm.devfactory.com windows_vdi_alias=windows_vdi

[windows-vdi:vars]
ansible_connection=winrm 
ansible_winrm_transport=ntlm
ansible_ssh_user=administrator
ansible_winrm_server_cert_validation=ignore
ansible_ssh_pass=ppuROilu&IK=?JgaQFxZ%3OboIUiTHk5

[all:vars]
yourkit_version=2018.04
yourkit_minor=b81

```

There are two entries for each target machine. First, the host (target) connection definitions, like its IP address. Then, the variables, which
define how to setup the connection. If the connection is secured by a SSH key to connect the variable `ansible_ssh_pass` is not required.


## OS Specific Playbooks

For each OS name and major distribution, there are three optional files that may be created:

* `{os-name}\[-major-version\]-pre-tasks.yml`

* `{os-name}\[-major-version\]-packages.yml`

* `{os-name}\[-major-version\]-post-tasks.yml`

Both the `os-version` and `major-version` are printed at the begining of `base.yml` play. Check if the required files exist in the `playbooks` directory.
If they don't exist, they will be skipped as no one is individually required. The major version of the file is optional. Therefore, both 
`Ubuntu-18.04-packages.yml` and `Ubuntu-packages.yml` are valid package list files for the Ubuntu distro. The former takes precedence on the later. 

`*-pre-tasks.yml` provides a list of tasks that must run at the begining of the play and `*-post-tasks.yml` lists define the tasks that must run at the end. They
may include every structure allowed in Playbook tasks. `*-packages.yml` is a list of packages available on the distro repository. The name of the packages may
be different depending on the distro. 


# Windows Setup

In order to a monitor computer to use Ansible for controlling a Windows host, it is necessary to follow some procedures. Mostly of the Windows related
are marked as "not stable interface" on Ansible, which means that Windows host monitoring may break due to updates. 

## Microsoft Windows Prerequisites for Ansible
1) PowerShell 3.0 or newer
2) Al least .NET 4.0

    * You can find detailed original post in below link.`https://docs.ansible.com/ansible/2.5/user_guide/windows_setup.html`
    * To check your powershell version; `$PSVersionTAble.PSVersion`

3) WinRM listener should be created and activated.

Connect to the VDI Instance and open a PowerShell. Then, execute the following commands:

```
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)

powershell.exe -ExecutionPolicy ByPass -File $file
```

Take note of the Thumbprint as it is going to be used later. To get information about the winrm listener and print the Thumbprint again, just run:

```
winrm enumerate winrm/config/Listener
```

After that, define the following variable:

```
$selector_set = @{
    Address = "*"
    Transport = "HTTPS"
}
```

Then, define the Thumbprint. Be careful to use the Thumbprint you took note before.

```
$value_set = @{
    CertificateThumbprint = "E6CDAA82EEAF2ECE8546E05DB7F3E01AA47D76CE"
}
```

Execute the following command to perform the final step.

```
New-WSManInstance -ResourceURI "winrm/config/Listener" -SelectorSet $selector_set -ValueSet $value_set
```

You can get information of the `winrm` service by running the following commands:

```
(Get-Service -Name winrm).Status

winrm get winrm/config/Service

winrm get winrm/config/Winrs
```
