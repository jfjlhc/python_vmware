#!/usr/bin/env python
from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
import atexit
import sys
import ssl

def delete_pool(pool_name):

    try:

        if hasattr(ssl, '_create_unverified_context'):  # check ssl has this context or not
            context = ssl._create_unverified_context()
        si = SmartConnect(host="192.168.134.231",
                          user="jfj",
                          pwd='pass2017!@#$',
                          port=443,
                          sslContext=context)
        if not si:
            print("Cannot connect to specified host using specified username and password")
            sys.exit()

        atexit.register(Disconnect, si)
        content = si.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.ResourcePool],
                                                          True)
        vmList = objView.view
        objView.Destroy()
        for pool in vmList:
            try:

                if pool.name == pool_name:
                    pool.Destroy()
            except Exception as e:
                print("no have this name :", str(e))


    except vmodl.MethodFault as e:
        print("Caught vmodl fault : " + e.msg)
    except Exception as e:
        print("Caught Exception : " + str(e))
