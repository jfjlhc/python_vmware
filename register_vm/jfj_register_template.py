#coding=utf-8
import atexit
import sys
import ssl
import atexit
import sys,time
import textwrap
from pyVim import connect
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import Resister_Vmfs_main as jfj

"""edit by jifujun"""

vc_host = "192.168.134.107"
vc_user = "jfj"
vc_passwd = "pass2017!@#$"
esxi_ip = "192.168.134.227"


def set_vc_si(host,user,port,password,context):
    try:
        si1 = SmartConnect(host=host, user=user,pwd=password,
                          port=port, sslContext=context)
        if not si1:
            #print ("Can't connect to the host with given user and password")
            sys.exit()

        atexit.register(Disconnect, si1)


    except Exception as e:
        sys,exit()
        #print ("catch the exception: ", str(e))
    return si1




def get_vc_si():
    host = vc_host
    user = vc_user
    password = vc_passwd
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




def waitForTask(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            #print("there was an error: %s" % task)
            pass
            task_done = True





def registerVM(virtualMachineFolder,folder,server, host, pool):
    registerTask=virtualMachineFolder.RegisterVM_Task(path =folder, name=server, asTemplate=False, pool = pool)
    waitForTask(registerTask)
    taskResult = registerTask.info.result
    return taskResult

def startVM(vm):
    print("powering on VM {0}", vm.name)
    if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:

        task = vm.PowerOn()

        answers = {}

        def handle_question(current_task, virtual_machine):

            if virtual_machine.runtime.question is not None:
                question_id = virtual_machine.runtime.question.id
                if question_id not in answers.keys():
                    answer = 2
                    print("\n".join(textwrap.wrap(vm.runtime.question.text, 60)))
                    answers[question_id] = answer
                    virtual_machine.AnswerVM(question_id, answer)

        while task.info.state != 'success' and task.info.state != 'error':
            handle_question(None,vm)
            #print(task.info.state)


        if task.info.state == vim.TaskInfo.State.error:

            print("error type: {0}", task.info.error.__class__.__name__)
            print("found cause: {0}", task.info.error.faultCause)
            for fault_msg in task.info.error.faultMessage:
                print(fault_msg.key)
                print(fault_msg.message)
            sys.exit(-1)

def _findpath(store):##match:*.vmx.* *.vmxf.* *.nvram.*
    s = "vmtx"
    array = []
    search = vim.HostDatastoreBrowserSearchSpec()
    details = vim.host.DatastoreBrowser.FileInfo.Details()
    details.fileType = True
    search.matchPattern = "*"
    search.details = details

    search_ds = store.browser.SearchDatastoreSubFolders_Task("[%s]" %store.summary.name, search)


    waitForTask(search_ds)
    results = search_ds.info.result

    for result in results:
        for file in result.file:
            if file.path.endswith("vmtx"):
                array.append(file.path[:-5])

    return array

def findpath(store,server):##match:*.vmx.* *.vmxf.* *.nvram.*
    search = vim.HostDatastoreBrowserSearchSpec()
    details = vim.host.DatastoreBrowser.FileInfo.Details()
    details.fileType = True
    search.matchPattern = server+".vmtx"
    search.details = details

    search_ds = store.browser.SearchDatastoreSubFolders_Task("[%s]" %store.summary.name, search)

    waitForTask(search_ds)
    results = search_ds.info.result

    for result in results:

        return result.folderPath
    return None

if __name__ == "__main__":
    try:
        instance = get_vc_si()
        atexit.register(connect.Disconnect, instance)
    except Exception as e:
        sys.exit()


    content = instance.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.Datacenter],
                                                      True)

    datacenter = objView.view[1]
    objView.Destroy()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    hosts = None
    for host in objView.view:
        if host.name == esxi_ip:
            hosts = host
            break
    objView.Destroy()

    datastores = hosts.datastore
    pool = hosts.resourcePool
    serverList = None
    host = hosts.host[0]

    fileManager = instance.content.fileManager
    virtualMachineFolder = datacenter.vmFolder


    for store in datastores:
        serverList = _findpath(store)

        for server in serverList:
            folder = findpath(store, server)

            if not folder:
                print("We did not get a valid folder path")
                sys.exit(1)

            folder = folder + "/%s.vmtx" % server
            print ("文件夹是：", folder)
            print ("--------------------------------------")
            try:
                machine = registerVM(virtualMachineFolder, folder, server, host, pool)
                machine.MarkAsTemplate()
            except Exception as e:
                pass
