import yaml
import os
import constants

class PlaybookCreator():


    def create(self, host_config, playbookDir):

        mainPlay = {}
        mainPlay['name'] = "Auto-generated Playbook for " + host_config['id']
        mainPlay['hosts'] = "{{ HOSTS }}"
        
        if ( host_config['os'] == 'windows' ):
            packager = 'win_chocolatey'
        else:
            packager = 'package'
            mainPlay['become'] = 'yes'
        
        taskList = []
        
        taskInfo = {
            "name": "Print Host OS",
            "debug": 'msg="Selected OS -> {{ ansible_distribution }}; Major version -> {{ ansible_distribution_major_version}}"'
        }
        taskList.append(taskInfo)
        
        
        if ('pre-tasks' in host_config):
            preTasks = {
                "name": "Execute preparation tasks",
                "include_tasks": "../" + host_config['pre-tasks']
            }
            taskList.append(preTasks)
        
        taskPackages = {
            "name": "Install OS pre-selected packages",
            packager: {
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
            packager: {
                "name": "{{ item }}",
                "state": "present"
            },
            "with_items": []
        }
            
        if ('additional_packages' in host_config):
            taskAdditional["with_items"] = host_config['additional_packages']
            taskList.append(taskAdditional)
        
        
        if ('post-tasks' in host_config):
            postTasks = {
                "name": "Execute post-installation tasks",
                "include_tasks": "../" + host_config['post-tasks']
            }
            taskList.append(postTasks)
        
        
        mainPlay['tasks'] = taskList
        
        if (not playbookDir[-1]  == '/'):
            playbookDir = playbookDir + '/'
        
        if not os.path.exists(playbookDir):
            os.makedirs(playbookDir)
                
        f = open(playbookDir + host_config['id'] + constants.PLAYBOOK_FILE_EXTENSION, 'w')
        
        yaml.safe_dump([mainPlay], f, default_flow_style=False)
