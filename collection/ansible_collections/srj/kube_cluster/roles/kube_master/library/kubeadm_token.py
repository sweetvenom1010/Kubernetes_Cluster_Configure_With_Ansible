#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - GOVIND BHARDWAJ (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from subprocess import getstatusoutput
except:
    from commands import getstatusoutput
from json import loads

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        action=dict(type='str',default="create",choices=["create","delete","generate"]),
        certificate_key=dict(type='str'),
        config=dict(type='str'),
        description=dict(type='str'),
        groups=dict(type='list',elements='str',default=['system:bootstrappers:kubeadm:default-node-token']),
        token=dict(type='str'),
        ttl=dict(type='str',default="24h0m0s"),
        usages=dict(type='list',elements='str',choices=["signing","authentication"],default=["signing","authentication"]),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message='',
        failed=False,
        token_info={}
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('action','create',('description',),True),
            ('action','delete',('token',),True),
            ],
    )
    cmd = "kubeadm token"
    action = module.params.pop('action')
    cmd = cmd + " " + action
    if action == 'delete':
        cmd = cmd + " " + module.params['token']
        result['cmd'] = cmd
        #module.exit_json(**result)
    else:
        for para in module.params.keys():
            if module.params[para] == None :
                continue
            elif  para == 'token':
                cmd = cmd + " " + module.params[para]
            elif isinstance(module.params[para],list):
                cmd = cmd + " " + "--" + para.replace("_","-")+ " "
                for element in module.params[para]:
                    cmd = cmd+element+","
                cmd = cmd.strip(",")
            else:
                cmd = cmd + " " + "--" + para.replace("_","-") + " " + str(module.params[para])
    token_info = (getstatusoutput("kubeadm token list -o json")[1]).split('}\n{')
    i=0
    if token_info[0] == '':
        del token_info[0]
    while i<len(token_info):
        #token_info[i]=token_info[i].replace('\n','')
        imd_var=i/2
        token_info[i]=token_info[i].rstrip("}")
        token_info[i]=token_info[i].lstrip("{")
        token_info[i] = token_info[i]+"}"
        token_info[i] = "{"+token_info[i]
        """
        if imd_var == int(imd_var):
            token_info[i]=token_info[i].rstrip("}")
            token_info[i] = token_info[i]+"}"
        else:
            token_info[i] = "{"+token_info[i]
        """
        #module.exit_json(**result)
        token_info[i]=loads(token_info[i])
        i+=1

    if action == "create":
        for token_element in token_info:
            if "description" in token_element.keys() and token_element["description"] == module.params["description"]:
                result["token_info"] = token_element
                output = ""
                break
        else:
            cmd = cmd + " " + "--print-join-command"
            status , output = getstatusoutput(cmd)
            if status == 0:
                result["join_command"] = output
                token_info = (getstatusoutput("kubeadm token list -o json")[1]).split('}\n{')
                i=0
                while i<len(token_info):
                    imd_var=i/2
                    token_info[i]=token_info[i].rstrip("}")
                    token_info[i]=token_info[i].lstrip("{")
                    token_info[i] = token_info[i]+"}"
                    token_info[i] = "{"+token_info[i]
                    token_info[i]=loads(token_info[i])
                    i+=1
                for token_element in token_info:
                    if "description" in token_element.keys() and token_element["description"] == module.params["description"]:
                        result["token_info"] = token_element
                        break
                result['changed']= True
    elif action == "delete":
        for token_element in token_info:
            if token_element["token"] == module.params["token"]:
                result["token_info"] = token_element
                delete_status , output = getstatusoutput(cmd)
                if delete_status == 0:
                    result['changed'] = True
                else:
                    result['failed'] = True
                break
        else:
            output = ""
    
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['message']=output

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['description'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
