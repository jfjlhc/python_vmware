#coding=utf-8
from pyVmomi import vim
import sys,atexit
import ssl
from pyVim.connect import SmartConnect, Disconnect

esxi_ip = "1.1.1.159"
netmask = "255.255.255.0"
gateway = "192.168.134.126"
macaddress = "00:50:56:6b:45:42"

def set_vc_si(host,user,port,password,context):
    try:
        si1 = SmartConnect(host=host, user=user,pwd=password,
                          port=port, sslContext=context)
        if not si1:
            print ("Can't connect to the host with given user and password")
            sys.exit()

        atexit.register(Disconnect, si1)


    except Exception as e:
        print ("catch the exception: ", str(e))
    return si1




def get_vc_si():
    host = "192.168.134.88"
    user = "root"
    password = "pass1234!@#$"
    port = 443
    if host:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    else:
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()


    si = set_vc_si(host, user, port, password, context)
    atexit.register(Disconnect, si)
    return si



def main():
    si = get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    host = objView.view
    objView.Destroy()


    nicspec = None
    for k in host[0].configManager.networkSystem.networkInfo.vnic:
        if k.spec.mac == macaddress:
            nicspec = k
            break;

    gatespec = host[0].configManager.networkSystem.ipRouteConfig

    nic = vim.host.VirtualNic.Config()
    nic.changeOperation = "edit"
    nic.device = "vmk1"
    nic.portgroup = "VMkernel"
    nic.spec = vim.host.VirtualNic.Specification()
    nic.spec.ip = vim.host.IpConfig()
    nic.spec.ip.ipAddress = esxi_ip
    nic.spec.ip.subnetMask = netmask
    nic.spec.ipRouteSpec = vim.host.VirtualNic.IpRouteSpec()


    myvnic = []
    myvnic.append(nic)
    myconfig=vim.host.NetworkConfig()
    myconfig.vnic=myvnic
    myconfig.ipRouteConfig = vim.host.IpRouteConfig()
    # myconfig.ipRouteConfig.defaultGateway = "192.168.134.126"
    # myconfig.ipRouteConfig.gatewayDevice = "vmnic1"


    host[0].configManager.networkSystem.UpdateNetworkConfig(changeMode="modify",config=myconfig)

    routespec = vim.host.IpRouteConfig()
    routespec.defaultGateway = gateway
    host[0].configManager.networkSystem.UpdateIpRouteConfig(config=routespec)


if __name__ == "__main__":
    main()
    print("esxi的ip地址修改完毕")
