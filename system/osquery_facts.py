#!/usr/bin/python -tt
#coding: utf-8 -*-

# (c) 2017, Richard Metzler
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '0.1'}

DOCUMENTATION = '''
---
module: osquery_facts
version_added: "2.3"
short_description: get facts from osquery selects
requirements: osqueryi in the PATH
description:
  - execute osquery selects and return the values
options:
  query:
    description:
      - The SELECT statement that is passed to osqueryi
    required: true
author:
  - "Richard Metzler (@rmetzler)"
'''

EXAMPLES = '''
- name: parse /etc/hosts
  osquery_facts:
    query: SELECT * FROM etc_hosts
  register: result

- debug: var=result
'''


from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(
        argument_spec={
            'query': {'required': True},
        },
        supports_check_mode=True,
    )

    query = module.params['query']
    command_options = [module.get_bin_path('osqueryi', True), query, '--json']
    command_result = module.run_command(command_options, check_rc=True)
    result = module.from_json(command_result[1])
    args = {
        'changed': False,
        'query': query,
        'value': result
    }
    module.exit_json(**args)

if __name__ == '__main__':
    main()
