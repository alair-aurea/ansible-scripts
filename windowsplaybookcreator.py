import yaml

class PlaybookCreator():

    def create(self, host_config, playbookDir):

        mainPlay = {}
        mainPlay['name'] = "Auto-generated Playbook for " + host_config['id']
        mainPlay['hosts'] = "{{ HOSTS }}"
        
        taskList = []
        
        taskInfo = {
            "name": "Print Host OS",
            "debug": 'msg="Selected OS -> {{ ansible_distribution }}; Major version -> {{ ansible_distribution_major_version}}"'
        }
        taskList.append(taskInfo)
        
        taskPackages = {
            "name": "Install OS pre-selected packages",
            "win_chocolatey": {
                "name": "{{ item }}",
                "state": "present"
            },
            "with_items": []
        }
        
        if ('packages' in host_config):
            taskPackages["with_items"] = host_config['packages']
            taskList.append(taskPackages)
        
        
        taskAdditional = {
            "name": "Install OS additional packages",
            "win_chocolatey": {
                "name": "{{ item }}",
                "state": "present"
            },
            "with_items": []
        }
            
        if ('additional_packages' in host_config):
            taskAdditional["with_items"] = host_config['additional_packages']
            taskList.append(taskAdditional)
        
        mainPlay['tasks'] = taskList
        
        if (not playbookDir[-1]  == '/'):
            playbookDir = playbookDir + '/'
            
        f = open(playbookDir + host_config['id'] + '.yml', 'w')
        
        yaml.safe_dump([mainPlay], f, default_flow_style=False)
