#coding=utf-8
from pyVmomi import vim
import sys,time
"""删除虚拟机"""
def create_vcenter_si():
    vcenter_ip = '192.168.134.98'
    vcenter_user = 'root'
    vcenter_pwd = 'pass1234!@#$'
    vcenter_port = 443
    si = None

    import ssl
    from pyVim import connect
    import atexit
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        si = connect.SmartConnect(host=vcenter_ip, user=vcenter_user, pwd=vcenter_pwd,
                                  port=vcenter_port, sslContext=ssl_context)
        atexit.register(connect.Disconnect, si)
    except Exception as e:
        print(str(e))
    return si

def main():
    si = create_vcenter_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == "192.168.134.21":
            objView = content.viewManager.CreateContainerView(host,
                                                              [vim.VirtualMachine],

                                                              True)
            vmList = objView.view
            objView.Destroy()
            for vm in vmList:
                print(vm.name)
                # vm.PowerOff()
                if not vm.resourcePool is None:
                    try:
                        if vm.runtime.powerState == "poweredOff":
                            vm.Destroy()
                            time.sleep(1)
                        else:
                            print("请先运行关闭虚拟机脚本，再来执行本程序")
                    except:
                        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
                        print(errormsg)


if __name__ == "__main__":
    main()
    print("DOing all.....")