# sethandlers.py


# trying to import various
def importVarious(context):
    
    if context.readDataFile('dove.various.txt') is None:
        return

    portal = context.getSite()
    #setup_plugin(portal)
