from pyVmomi import vim
import sys,time
"""虚拟机转换成模板"""
def create_vcenter_si():
    vcenter_ip = '192.168.134.231'
    vcenter_user = 'jfj'
    vcenter_pwd = 'pass2017!@#$'
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
        if host.name == "192.168.134.99":
            objView = content.viewManager.CreateContainerView(host,
                                                              [vim.ResourcePool],

                                                              True)
            vmList = objView.view
            objView.Destroy()

            for pool in vmList:
                if pool.name == "jfj_server":
                    objView = content.viewManager.CreateContainerView(pool,
                                                                      [vim.VirtualMachine],

                                                                      True)
                    vmList = objView.view
                    objView.Destroy()
                    for vm in vmList:
                        if vm.name == "WIN7o":
                            vm.MarkAsTemplate()

if __name__ == "__main__":
    main()
    print("DOing all.....")