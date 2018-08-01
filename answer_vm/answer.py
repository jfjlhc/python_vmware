# coding=utf-8
import ssl
import atexit
import sys, time
from pyVim import connect
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import os

"""edit by jifujun"""

esxi_host = "192.168.137.67"
esxi_user = "root"
esxi_passwd = "pass1234!@#$"


def set_vc_si(host, user, port, password, context):
    si1=None
    try:
        si1 = SmartConnect(host=host, user=user, pwd=password,
                           port=port, sslContext=context)
        if not si1:
            print("Can't connect to the host with given user and password")
            sys.exit()

        atexit.register(Disconnect, si1)


    except Exception as e:
        print("catch the exception: ", str(e))
    return si1


def get_vc_si():
    host = esxi_host
    user = esxi_user
    password = esxi_passwd
    port = 8081
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


instance = get_vc_si()
atexit.register(connect.Disconnect, instance)


def waitForTask(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            pass
            task_done = True


def registerVM(virtualMachineFolder, folder, server, host, pool):
    registerTask = virtualMachineFolder.RegisterVM_Task(path=folder, name=server, asTemplate=False, pool=pool)
    waitForTask(registerTask)
    taskResult = registerTask.info.result
    return taskResult


def startVM(vm):
    print("powering on VM %s"%(vm.name))

    if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:

        task = vm.PowerOn()
        time.sleep(2)

        def handle_question(current_task, virtual_machine):
            if virtual_machine.runtime.question is not None:
                question_id = virtual_machine.runtime.question.id
                vm.AnswerVM(questionId=question_id,answerChoice="2")

        while task.info.state != 'success' and task.info.state != 'error':
            handle_question(None, vm)


        if task.info.state == vim.TaskInfo.State.error:

            print("error type: {0}", task.info.error.__class__.__name__)
            print("found cause: {0}", task.info.error.faultCause)
            for fault_msg in task.info.error.faultMessage:
                print(fault_msg.key)
                print(fault_msg.message)
            sys.exit(-1)


def _findpath(store):  ##match:*.vmx.* *.vmxf.* *.nvram.*
    s = "vmx"
    array = []
    search = vim.HostDatastoreBrowserSearchSpec()
    details = vim.host.DatastoreBrowser.FileInfo.Details()
    details.fileType = True
    search.matchPattern = "*"
    search.details = details

    search_ds = store.browser.SearchDatastoreSubFolders_Task("[%s]" % store.summary.name, search)

    waitForTask(search_ds)
    results = search_ds.info.result

    for result in results:
        for file in result.file:
            if file.path.endswith("vmx"):
                array.append(file.path[:-4])

    return array


def findpath(store, server):  ##match:*.vmx.* *.vmxf.* *.nvram.*
    search = vim.HostDatastoreBrowserSearchSpec()
    details = vim.host.DatastoreBrowser.FileInfo.Details()
    details.fileType = True
    search.matchPattern = server + ".vmx"
    search.details = details

    search_ds = store.browser.SearchDatastoreSubFolders_Task("[%s]" % store.summary.name, search)

    waitForTask(search_ds)
    results = search_ds.info.result

    for result in results:
        return result.folderPath
    print()
    return None

def seepath(store):  ##match:*.vmx.* *.vmxf.* *.nvram.*
    s = "vmx"
    array = []
    search = vim.HostDatastoreBrowserSearchSpec()
    details = vim.host.DatastoreBrowser.FileInfo.Details()
    details.fileType = True
    search.matchPattern = "*"
    search.details = details

    search_ds = store.browser.SearchDatastoreSubFolders_Task("[%s]" % store.summary.name, search)

    waitForTask(search_ds)
    results = search_ds.info.result

    for result in results:
        for file in result.file:
            print(file)


if __name__ == "__main__":

    content = instance.RetrieveServiceContent()
    datacenter = instance.content.rootFolder.childEntity[0]
    datastores = datacenter.datastore
    pool = datacenter.hostFolder.childEntity[0].resourcePool

    serverList = None



    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vm = None
    for vm in objView.view:
         #print(vm.name)
         #print(vm.runtime.connectionState)
    #print()
        if vm.runtime.connectionState == "inaccessible":
            vm.UnregisterVM()



    for vm in objView.view:
        #print(vm.runtime.connectionState)

        if vm.runtime.connectionState == "orphaned":
            vm.UnregisterVM()
    objView.Destroy()


    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    hostname = None
    for hosts in objView.view:
        if hosts.name == "localhost.localdomain":
            hostname = hosts

            break
    objView.Destroy()

    host = hostname

    fileManager = instance.content.fileManager
    virtualMachineFolder = datacenter.vmFolder
    serverLists = []

    array = []
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmobj = None


    for vmobj in objView.view:
        array.append(vmobj)
    objView.Destroy()

    # print(array)
    # print()
    if len(array) > 5:
        #print()
        for vm in array:
            if vm.runtime.question is not None:
                question_id = vm.runtime.question.id
                vm.AnswerVM(questionId=question_id, answerChoice="2")
            else:
                if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
                    task = vm.PowerOn()
                    waitForTask(task)
    else:

        for store in datastores:
            serverLists = _findpath(store)
            daname = store.name
            #path = seepath(store)
            try:
                for server in serverLists:
                    # pass
                    folder = "[%s]" % daname + " " + server
                    folder = folder + "/%s.vmx" % server
                    print(folder)
                    print("现在开始添加虚拟机到清单：")
                    # print(virtualMachineFolder, folder, server, host, pool)
                    machine = registerVM(virtualMachineFolder, folder, server, host, pool)
                    #startVM(machine)



            except Exception as e:
                print(e)


    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                       [vim.VirtualMachine],
                                                       True)

    for vm in objView.view:
        startVM(vm)
    objView.Destroy()
    os.system("python jfj_register_template.py")
    print("程序已结束！")



