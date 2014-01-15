from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time, sys

DEVICE="/dev/ttyUSB0"

options = ZWaveOption(DEVICE, config_path="/home/domotika/plugins/zwave/openzwave/", 
         user_path="/home/domotika/plugins/zwave/user", cmd_line="")
options.set_log_file("/home/domotika/logs/OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
#options.set_logging("Debug")
options.set_logging("Error")
options.lock()

#Create a network object
network = ZWaveNetwork(options, log=None)

time_started = 0
print "------------------------------------------------------------"
print "Waiting for network awaked : "
print "------------------------------------------------------------"
for i in range(0,300):
    if network.state>=network.STATE_AWAKED:

        print(" done")
        print("Memory use : %s Mo" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time_started += 1
        time.sleep(1.0)
if network.state<network.STATE_AWAKED:
    print "."
    print "Network is not awake but continue anyway"
print "------------------------------------------------------------"
print "Use openzwave library : %s" % network.controller.ozw_library_version
print "Use python library : %s" % network.controller.python_library_version
print "Use ZWave library : %s" % network.controller.library_description
print "Network home id : %s" % network.home_id_str
print "Controller node id : %s" % network.controller.node.node_id
print "Controller node version : %s" % (network.controller.node.version)
print "Nodes in network : %s" % network.nodes_count
print "------------------------------------------------------------"
print "Waiting for network ready : "
print "------------------------------------------------------------"
for i in range(0,300):
    if network.state>=network.STATE_READY:
        print " done in %s seconds" % time_started
        break
    else:
        sys.stdout.write(".")
        time_started += 1
        #sys.stdout.write(network.state_str)
        #sys.stdout.write("(")
        #sys.stdout.write(str(network.nodes_count))
        #sys.stdout.write(")")
        #sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if not network.is_ready:
    print "."
    print "Network is not ready but continue anyway"
print "------------------------------------------------------------"
print "Controller capabilities : %s" % network.controller.capabilities
print "Controller node capabilities : %s" % network.controller.node.capabilities
print "Nodes in network : %s" % network.nodes_count
print "Driver statistics : %s" % network.controller.stats
print "------------------------------------------------------------"
for node in network.nodes:
    print
    print "------------------------------------------------------------"
    print "%s - Name : %s" % (network.nodes[node].node_id,network.nodes[node].name)
    print "%s - Manufacturer name / id : %s / %s" % (network.nodes[node].node_id,network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id)
    print "%s - Product name / id / type : %s / %s / %s" % (network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type)
    print "%s - Version : %s" % (network.nodes[node].node_id, network.nodes[node].version)
    print "%s - Command classes : %s" % (network.nodes[node].node_id,network.nodes[node].command_classes_as_string)
    print "%s - Capabilities : %s" % (network.nodes[node].node_id,network.nodes[node].capabilities)
    print "%s - Neigbors : %s" % (network.nodes[node].node_id,network.nodes[node].neighbors)
    print "%s - Can sleep : %s" % (network.nodes[node].node_id,network.nodes[node].can_wake_up())
    groups = {}
    for grp in network.nodes[node].groups :
        groups[network.nodes[node].groups[grp].index] = {'label':network.nodes[node].groups[grp].label, 'associations':network.nodes[node].groups[grp].associations}
    print "%s - Groups : %s" % (network.nodes[node].node_id, groups)
    values = {}
    for val in network.nodes[node].values :
        values[network.nodes[node].values[val].object_id] = {
            'label':network.nodes[node].values[val].label,
            'help':network.nodes[node].values[val].help,
            'command_class':network.nodes[node].values[val].command_class,
            'max':network.nodes[node].values[val].max,
            'min':network.nodes[node].values[val].min,
            'units':network.nodes[node].values[val].units,
            'data':network.nodes[node].values[val].data_as_string,
            'ispolled':network.nodes[node].values[val].is_polled
            }
    #print "%s - Values : %s" % (network.nodes[node].node_id, values)
    #print "------------------------------------------------------------"
    for cmd in network.nodes[node].command_classes:
        print "   ---------   "
        #print "cmd = ",cmd
        values = {}
        for val in network.nodes[node].get_values_for_command_class(cmd) :
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'help':network.nodes[node].values[val].help,
                'max':network.nodes[node].values[val].max,
                'min':network.nodes[node].values[val].min,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data,
                'data_str':network.nodes[node].values[val].data_as_string,
                'genre':network.nodes[node].values[val].genre,
                'type':network.nodes[node].values[val].type,
                'ispolled':network.nodes[node].values[val].is_polled,
                'readonly':network.nodes[node].values[val].is_read_only,
                'writeonly':network.nodes[node].values[val].is_write_only,
                }
        print "%s - Values for command class : %s : %s" % (network.nodes[node].node_id,
                                    network.nodes[node].get_command_class_as_string(cmd),
                                    values)
    print "------------------------------------------------------------"
print
print "------------------------------------------------------------"
print "Driver statistics : %s" % network.controller.stats
print "------------------------------------------------------------"
print
print "------------------------------------------------------------"
print "Try to autodetect nodes on the network"
print "------------------------------------------------------------"
print "Nodes in network : %s" % network.nodes_count
print "------------------------------------------------------------"
print "Retrieve switches on the network"
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  state: %s" % (network.nodes[node].get_switch_state(val)))
print "------------------------------------------------------------"
print "Retrieve dimmers on the network"
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_dimmers() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  level: %s" % (network.nodes[node].get_dimmer_level(val)))
print "------------------------------------------------------------"
print "Retrieve sensors on the network"
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_sensors() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  value: %s %s" % (network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units))
print "------------------------------------------------------------"
print "Retrieve switches all compatibles devices on the network    "
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches_all() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  value / items: %s / %s" % (network.nodes[node].get_switch_all_item(val), network.nodes[node].get_switch_all_items(val)))
        print("  state: %s" % (network.nodes[node].get_switch_all_state(val)))
print "------------------------------------------------------------"
print "Retrieve protection compatibles devices on the network    "
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_protections() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  value / items: %s / %s" % (network.nodes[node].get_protection_item(val), network.nodes[node].get_protection_items(val)))
print "------------------------------------------------------------"

print "------------------------------------------------------------"
print "Retrieve battery compatibles devices on the network         "
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_battery_levels() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  value : %s" % (network.nodes[node].get_battery_level(val)))
print "------------------------------------------------------------"

print "------------------------------------------------------------"
print "Retrieve power level compatibles devices on the network         "
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_power_levels() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  value : %s" % (network.nodes[node].get_power_level(val)))
print "------------------------------------------------------------"
#print
#print "------------------------------------------------------------"
#print "Activate the switches on the network"
#print "Nodes in network : %s" % network.nodes_count
#print "------------------------------------------------------------"
#for node in network.nodes:
#    for val in network.nodes[node].get_switches() :
#        print("Activate switch %s on node %s" % \
#                (network.nodes[node].values[val].label,node))
#        network.nodes[node].set_switch(val,True)
#        print("Sleep 10 seconds")
#        time.sleep(10.0)
#        print("Dectivate switch %s on node %s" % \
#                (network.nodes[node].values[val].label,node))
#        network.nodes[node].set_switch(val,False)
#print "%s" % ('Done')
#print "------------------------------------------------------------"

print
print "------------------------------------------------------------"
print "Driver statistics : %s" % network.controller.stats
print "Driver label : %s" % \
    network.controller.get_stats_label('retries')
#print "------------------------------------------------------------"
#print
#print "------------------------------------------------------------"
#print "Stop network"
#print "------------------------------------------------------------"
#network.stop()

