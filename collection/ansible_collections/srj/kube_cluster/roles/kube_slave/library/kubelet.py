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
from subprocess import getoutput

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        add_dir_header=dict(type='bool',default=False),
        application_metrics_count_limit=dict(type='int',default=100),
        azure_container_registry_config=dict(type='str'),
        boot_id_file=dict(type='str',default="/proc/sys/kernel/random/boot_id"),
        bootstrap_kubeconfig=dict(type='str'),
        cert_dir=dict(type='str',default="/var/lib/kubelet/pki"),
        chaos_chance=dict(type='float'),
        cloud_config=dict(type='str'),
        cloud_provider=dict(type='str'),
        cni_bin_dir=dict(type='str',default="/opt/cni/bin"),
        cni-cache_dir=dict(type='str',default="/var/lib/cni/cache"),
        cni-conf_dir=dict(type='str',default="/etc/cni/net.d"),
        config=dict(type='str'),
        container_hints=dict(type='str',default="/etc/cadvisor/container_hints.json"),
        container_runtime=dict(type='str',default="docker",choices=["docker","remote"]),
        containerd=dict(type='str',default="/run/containerd/containerd.sock"),
        containerd_namespace=dict(type='str',default="k8s.io"),
        docker=dict(type='str',default="unix:///var/run/docker.sock"),
        docker_endpoint=dict(type='str',default="unix:///var/run/docker.sock"),
        docker_env_metadata_whitelist=dict(type='str'),
        docker_only=dict(type='str',default="no",choices=["yes","no"]),
        docker_root=dict(type='str',default="/var/lib/docker"),
        docker_tls=dict(type='str',default="no",choices=["yes","no"]),
        docker_tls_ca=dict(type='str',default="ca.pem"),
        docker_tls_cert=dict(type='str',default="cert.pem"),
        docker_tls_key=dict(type='str',default="key.pem"),
        dynamic_config_dir=dict(type='str'),
        enable_cadvisor_json_endpoints=dict(type='bool',default=False),
        enable_load_reader=dict(type='str'),
        event_storage_age_limit=dict(type='str',default="0"),
        event-storage-event-limit=dict(type='str',default="0"),
        exit_on_lock_contention=dict(type='str',default="no",choices=["yes","no"]),
        fail_swap_on=dict(type='bool',default=True),
        global_housekeeping_interval=dict(type='str',default="1m0s"),
        hostname_override=dict(type='str'),
        housekeeping_interval=dict(type='str',default="10s"),
        image_credential_provider_bin_dir=dict(type='str'),
        image_credential_provider_config=dict(type='str'),
        image_pull_progress_deadline=dict(type='str',default="1m0s"),
        keep_terminated_pod_volumes=dict(type='str'),
        kubeconfig=dict(type='str'),
        lock_file=dict(type='str'),
        log_backtrace_at=dict(type='str',default="0"),
        log_cadvisor_usage=dict(type='str',default="no",choices=["yes","no"]),
        log_dir=dict(type='str'),
        log_file=dict(type='str'),
        log_file_max_size=dict(type='int',default=1800),
        log_flush_frequency=dict(type='str',default="5s"),
        logtostderr=dict(type='bool',default=True),
        machine_id_file=dict(type='str',default="/etc/machine-id,/var/lib/dbus/machine-id"),
        master_service_namespace=dict(type='str'),
        maximum_dead_containers=dict(type='str',default="-1"),
        maximum_dead_containers_per_container=dict(type='str',default="1"),
        minimum_container_ttl_duration=dict(type='str'),
        minimum_image_ttl_duration=dict(type='str',default="2m0s"),
        network_plugin=dict(type='str'),
        network_plugin_mtu=dict(type='int',default=1460),
        node_ip=dict(type='str'),
        node_labels=dict(type='dict'),
        non_masquerade_cidr=dict(type='str',default="10.0.0.0/8"),
        #one-output
        pod_infra_container_image=dict(type='str',default="k8s.gcr.io/pause:3.2"),
        register_node=dict(type='bool',default=True),
        register_schedulable=dict(type='bool',default=True),
        #register_with_taints=dict(type='list'),
        root_dir=dict(type='str',default="/var/lib/kubelet"),
        runtime_cgroups=dict(type='str'),
        seccomp_profile_root=dict(type='str',default="/var/lib/kubelet/seccomp"),
        storage_driver_buffer_duration=dict(type='str',default="1m0s"),
        storage_driver_db=dict(type='str',default="cadvisor"),
        storage_driver_host=dict(type='str',default="localhost:8086"),
        storage_driver_password=dict(type='str',default="root"),
        storage_driver_secure=dict(type='str',default="no",choices=["yes","no"]),
        storage_driver_table=dict(type='str',default="stats"),
        storage_driver_user=dict(type='str',default="root"),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    cmd = "kubeadm init "
    for para in module.params.keys():
        if module.params[para] == None :
            continue
        if module.params[para] == "yes":
            cmd = cmd + " " + "--" + para.replace("_","-")
        else:
            cmd = cmd + " " + "--" + para.replace("_","-") + " " + str(module.params[para])

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['pod_network_cidr']
    result['message'] = getoutput(cmd)

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['pod_network_cidr'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
