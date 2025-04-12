
.. image:: https://travis-ci.com/mkorman90/regipy.svg?branch=master
    :target: https://travis-ci.com/mkorman90/regipy

regipy
==========
Regipy is a python library for parsing offline registry hives!

Features:

* Use as a library
* Recurse over the registry hive, from root or a given path and get all subkeys and values
* Read specific subkeys and values
* Apply transaction logs on a registry hive
* Command Line Tools:
    * Dump an entire registry hive to json
    * Apply transaction logs on a registry hive
    * Compare registry hives
    * Execute plugins from a robust plugin system (i.e: amcache, shimcache, extract computer name...)

:Project page: https://github.com/mkorman90/regipy

Using as a library:
--------------------
.. code:: python

    from regipy.registry import RegistryHive
    reg = RegistryHive('/Users/martinkorman/Documents/TestEvidence/Registry/Vibranium-NTUSER.DAT')

    # Iterate over a registry hive recursively:
    for entry in reg.recurse_subkeys(as_json=True):
        print(entry)

    # Iterate over a key and get all subkeys and their modification time:
    for sk in reg.get_key('Software').get_subkeys():
        print(sk.name, convert_wintime(sk.header.last_modified).isoformat())

    # Get values from a specific registry key:
    reg.get_key('Software\Microsoft\Internet Explorer\BrowserEmulation').get_values(as_json=True)

    # Use plugins:
    from regipy.plugins.ntuser.ntuser_persistence import NTUserPersistencePlugin
    NTUserPersistencePlugin(reg, as_json=True).run()

    # Run all supported plugins on a registry hive:
    run_relevant_plugins(reg, as_json=True)

Install
^^^^^^^
Install regipy and the command line tools dependencies:

``pip install regipy[cli]``


NOTE: using pip with ``regipy[cli]`` instead of the plain ``regipy`` is a
significant change from version 1.9.x

For using regipy as a library, install only ``regipy`` which comes with fewer
dependencies:

``pip install regipy``
