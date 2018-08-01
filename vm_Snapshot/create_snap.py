#coding=utf-8
from pyVmomi import vmodl
from pyVmomi import vim
import sys,atexit
import ssl
from pyVim.connect import SmartConnect, Disconnect

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
    host = "192.168.134.99"
    user = "root"
    password = "JcatPass0197"
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


def WaitForTasks(tasks, si):
    """
    Given the service instance si and tasks, it returns after all the
    tasks are complete
    """

    pc = si.content.propertyCollector

    taskList = [str(task) for task in tasks]

    # Create filter
    objSpecs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task) for task in tasks]
    propSpec = [vmodl.query.PropertyCollector.PropertySpec(type=vim.Task, pathSet=[], all=True)]
    filterSpec = vmodl.query.PropertyCollector.FilterSpec(objectSet=objSpecs, propSet=propSpec)
    filter = pc.CreateFilter(filterSpec, True)

    try:
        version, state = None, None

        # Loop looking for updates till the state moves to a completed state.
        while len(taskList):
            update = pc.WaitForUpdates(version)
            for filterSet in update.filterSet:
                for objSet in filterSet.objectSet:
                    task = objSet.obj
                    for change in objSet.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in taskList:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            taskList.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if filter:
            filter.Destroy()

def Create_snap(resourcePool,si):

    try:
        if resourcePool.name == "Hy_Os":
            print("yes")
            name = "jfjnew"
            # for vm in resourcePool.vm:
            #     name = name + "1"
            tasks = [vm.CreateSnapshot(name=vm.name+"j",description="This is jfj snap~",memory=False,quiesce=True)
                     for vm in resourcePool.vm]
            WaitForTasks(tasks,si)
            print("Virtual Machine(s) have been snapshop on successfully")
    except Exception as e:
        print("no have this name :", str(e))



def main():
    si = get_vc_si()

    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ResourcePool],
                                                      True)
    vmList = objView.view
    objView.Destroy()
    for i in vmList:
        print(i.name)
        if i.name == "Hy_Os":
            Create_snap(i,si)


if __name__ == "__main__":
    main()
    print("DOing all.....")