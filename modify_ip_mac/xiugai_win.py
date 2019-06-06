#!/usr/bin/env python3
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from getpass import getpass
import ssl
import atexit
import argparse
import sys
"""更改WINDOWS地址"""
def options():

    parser = argparse.ArgumentParser(prog='exec-guestos-cmd',
                                     add_help=True)
    parser.add_argument('--host', '-vc',
                        type=str, default='192.168.134.99')
    parser.add_argument('--username', '-u',
                        type=str, default='root')
    parser.add_argument('--password', '-p',
                        type=str, default='JcatPass0197')
    parser.add_argument('--targetvm', '-tvm',
                        type=str, default='win 7_network')
    parser.add_argument('--guestuser', '-gu',
                        type=str, default='Administrator',
                        help='指定客户操作系统用户')
    parser.add_argument('--guestpassword', '-gp',
                        type=str, default='pass1234!@#$',
                        help='指定来宾操作系统的用户密码')
    args = parser.parse_args()
    if(not(args.password)):
        args.password = getpass(prompt='vCenter Password:')

    if(not(args.guestpassword)):
        args.guestpassword = getpass(prompt='Guest OS Password:')

    return args
def get_mob_info(content, mob, target=''):

    r = content.viewManager.CreateContainerView(content.rootFolder,
                                                [mob],
                                                True)

    if(target):
        for i in r.view:
            if(i.name == target):
                r = i

    return r

def login(args):

    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()

    si = SmartConnect(host = args.host,
                      user = args.username,
                      pwd = args.password,
                      sslContext = context)


    atexit.register(Disconnect, si)


    content = si.content

    return content

def check_vmware_tools_status(vm_mob):

    vmware_tools_status = vm_mob.guest.toolsStatus
    if(not(vmware_tools_status == 'toolsOk')):
        sys.stderr.write("%s: VMware tools\n" % vm_mob.name)
        sys.exit(1)

def main(args):
    # ServiceContent.
    content = login(args)


    vm_mob = get_mob_info(content, vim.VirtualMachine, args.targetvm)
    check_vmware_tools_status(vm_mob)

    guest_auth = vim.vm.guest.NamePasswordAuthentication()
    guest_auth.username = args.guestuser
    guest_auth.password = args.guestpassword

    guest_program_spec = vim.vm.guest.ProcessManager.ProgramSpec()
    guest_program_spec.arguments = '/c  echo SSSSSSaaa > c:\kktest\jtest.txt  '

    guest_program_spec.programPath = 'C:\Windows\system32\cmd.exe'
    # guest_program_spec.arguments = 'cmd /c netsh interface ip set address "本地连接" ' \
    #                                'static 192.168.134.76 255.255.255.192 192.168.134.65 '
    # guest_program_spec.programPath = 'C:\Windows\system32\cmd.exe'

    # guest_program_spec2 = vim.vm.guest.ProcessManager.ProgramSpec()
    # guest_program_spec2.arguments = 'cmd /c netsh interface ip set dns "本地连接" static 114.114.114.114 '
    # guest_program_spec2.programPath = 'C:\Windows\system32\cmd.exe'
    #
    # guest_program_spec3 = vim.vm.guest.ProcessManager.ProgramSpec()
    # guest_program_spec3.arguments = 'cmd /c netsh interface ip set address "本地连接 2" ' \
    #                                 'static 192.168.60.78 255.255.255.192 192.168.60.1 '
    # guest_program_spec3.programPath = 'C:\Windows\system32\cmd.exe'
    #
    # guest_program_spec4 = vim.vm.guest.ProcessManager.ProgramSpec()
    # guest_program_spec4.arguments = 'cmd /c netsh interface ip set dns "本地连接 2" static 114.114.114.114 '
    # guest_program_spec4.programPath = 'C:\Windows\system32\cmd.exe'

    r = content.guestOperationsManager.processManager.StartProgramInGuest(
        vm=vm_mob,
        auth=guest_auth,
        spec=guest_program_spec
    )

    # b = content.guestOperationsManager.processManager.StartProgramInGuest(
    #     vm=vm_mob,
    #     auth=guest_auth,
    #     spec=guest_program_spec2
    # )
    # c = content.guestOperationsManager.processManager.StartProgramInGuest(
    #     vm=vm_mob,
    #     auth=guest_auth,
    #     spec=guest_program_spec3
    # )
    # d = content.guestOperationsManager.processManager.StartProgramInGuest(
    #     vm=vm_mob,
    #     auth=guest_auth,
    #     spec=guest_program_spec4
    # )
    print(r)

if __name__ == '__main__':
    args = options()
    main(args)