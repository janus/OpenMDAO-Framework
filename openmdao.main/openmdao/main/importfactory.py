"""
This module contains the ImportFactory class, which uses the 
normal python import mechanism to find a module with a given name. It 
assumes that the module contains a factory function or class with the same
name as the module's local name, i.e., not the full package path.
"""

#public symbols
__all__ = ["ImportFactory"]

__version__ = "0.1"


from openmdao.main.factory import Factory
from openmdao.main.logger import logger
   
class ImportFactory(Factory):
    """Creates objects using the standard python __import__ mechanism. The 
    object must have a ctor with the same name as the module, minus the file 
    extension.  For example, to create a MyComp object, the module must be 
    named MyComp.py (or .pyc or .pyo). This factory does not support specific 
    version creation or creation on a remote server."""

    def __init__(self):
        Factory.__init__(self)
        self._ctors = {}

    def create(self, typ, name=None, version=None, server=None, 
               res_desc=None):
        """tries to import the given named module and return a factory 
        function from it. The factory function or constructor must have the same
        name as the module. The module must be importable in the current python
        environment.
        """
                
        if server is not None or version is not None:
            return None
        if res_desc is not None and len(res_desc)>0:
            return None
        
        if typ not in self._ctors:
            parts = typ.split('.')
            cname = parts[-1]
            modname = '.'.join(parts[:-1])
            try:
                mod = __import__(modname, globals(), locals(), [cname])
            except ImportError, err:
                logger.debug(str(err))
                return None
            try:
                self._ctors[typ] = getattr(mod, cname)
            except AttributeError, err:
                logger.debug(str(err))
                return None
        
        return self._ctors[typ](name)
    