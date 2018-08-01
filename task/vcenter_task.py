#coding=utf-8
from pyVmomi import vim,vmodl

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
            return ("子任务结束，可以进行下一轮任务")