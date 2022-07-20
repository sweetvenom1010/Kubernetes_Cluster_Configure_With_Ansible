#!/usr/bin/python3

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
    apiserver_advertise_address:
        description: The IP address the API Server will advertise it's listening on. If not set the default network interface will be used.
        required: false
        type: str
    apiserver_bind_port:
        description: Port for the API Server to bind to.
        required: false
        type: int
        default: 6443
    apiserver_cert_extra_sans:
        description: Optional extra Subject Alternative Names (SANs) to use for the API Server serving certificate. Can be both IP addresses and DNS names.
        required: false
        type: str
    cert_dir:
        description: The path where to save and store the certificates.
        required: false
        type: str
        default: "/etc/kubernetes/pki"
    certificate_key:
        description: Key used to encrypt the control-plane certificates in the kubeadm-certs Secret.
        required: false
        type: str
    config:
        description: Path to a kubeadm configuration file.
        required: false
        type: str
    control_plane_endpoint:
        description: Specify a stable IP address or DNS name for the control plane.
        required: false
        type: str
    cri_socket:
        description: Path to the CRI socket to connect. If empty kubeadm will try to auto-detect this value; use this option only if you have more than one CRI installed or if you have non-standard CRI socket.
        required: false
        type: str
    experimental_patches:
        description: Path to a directory that contains files named "target[suffix][+patchtype].extension". For example, "kube-apiserver0+merge.yaml" or just "etcd.json". "patchtype" can be one of "strategic", "merge" or "json" and they match the patch formats supported by kubectl. The default "patchtype" is "strategic". "extension" must be either "json" or "yaml". "suffix" is an optional string that can be used to determine which patches are applied first alpha-numerically.
        required: false
        type: str
    feature_gates:
        description: A set of key=value pairs that describe feature gates for various features.
        required: false
        type: dict
        options:
            IPv6DualStack:
                required: false
                type: bool
                default: false
            PublicKeysECDSA:
                required: false
                type: bool
                default: false
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
    - GOVIND BHARDWAJ (@govi230)
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
except ImportError:
    from commands import getstatusoutput

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        apiserver_advertise_address=dict(type='str'),
        apiserver_bind_port=dict(type='int',default=6443),
        apiserver_cert_extra_sans=dict(type='str'),
        cert_dir=dict(type='str',default="/etc/kubernetes/pki"),
        certificate_key=dict(type='str'),
        config=dict(type='str'),
        control_plane_endpoint=dict(type='str'),
        cri_socket=dict(type='str'),
        experimental_patches=dict(type='str'),
        feature_gates=dict(type='dict',options=dict(
            IPv6DualStack=dict(type='bool',default=True),
            PublicKeysECDSA=dict(type='bool',default=True)
            )),
        ignore_preflight_errors=dict(type='list'),
        image_repository=dict(type='str',default="k8s.gcr.io"),
        kubernetes_version=dict(type='str',default="stable-1"),
        node_name=dict(type='str'),
        pod_network_cidr=dict(type='str',required=True),
        service_cidr=dict(type='str',default="10.96.0.0/12"),
        service_dns_domain=dict(type='str',default="cluster.local"),
        #skip_certificate_key_print=dict(type='str',required=False),
        skip_phases=dict(type='str'),
        #skip-token-print
        token=dict(type='str'),
        token_ttl=dict(type='str',default="24h0m0s"),
        upload_certs=dict(type='str',default="no",choices=["yes","no"])
        #add-dir-header
        #log-file
        #log-file-max-size
        #one-output
        #skip-headers
        #skip-log-headers
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message='',
        failed=False
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
        if module.params[para] == None or  module.params[para] == "no":
            continue
        elif module.params[para] == "yes":
            cmd = cmd + " " + "--" + para.replace("_","-")
        elif para == "ignore_preflight_errors":
            for element in module.params[para]:
                cmd = cmd + " " + "--" + para.replace("_","-") + " " + str(element)
        else:
            cmd = cmd + " " + "--" + para.replace("_","-") + " " + str(module.params[para])

    if getstatusoutput("kubectl cluster-info")[0] != 0:
        getstatusoutput("kubeadm reset --force")
        status , output = getstatusoutput(cmd)
        if status==0:
            result["changed"] = True
        else:
            result["failed"] = True
    else:
        output = "Kubernetes Master is already Initialized"
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = cmd
    result['message'] = output

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
