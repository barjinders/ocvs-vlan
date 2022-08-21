###########################################################
#  Author - Barjinder Singh                               #
#  mail.barjinder@gmail.com                               #
#  https://www.linkedin.com/in/barjinder-singh-48357555/  #                              
# #########################################################                              


from itertools import count
import oci
import json
from datetime import datetime
import time


start = datetime.now()
config = oci.config.from_file("~/.oci/configp", "DEFAULT")
# open the JSON file
f = open('/Users/barjindersingh/Documents/vrf-code/userInputs.json')
# parse the JSON file
try:
    data = json.load(f)
except json.decoder.JSONDecodeError:
    print("Invalid documentTemplate JSON")


# Initialize service network client with default config file
core_client = oci.core.VirtualNetworkClient(config)

# Initialize service compute client with default config file
core_compute_client = oci.core.ComputeClient(config)

#### Function to create a route table ######################
def create_rt_table(core_client, rtconfig, defined_tags, freeform_tags):
    # Create a DRG
    print("Creating route table \"{}\"...".format(rtconfig["routeTableConfig"]["display_name"]))
    rtRulesAry = []
    rtRules = rtconfig["routeRules"]
    for rtRule in rtRules:
        rtRulesAry.append(
            oci.core.models.RouteRule(
            network_entity_id= rtRule["network_entity_id"],
            destination= rtRule["destination"],
            description= rtRule["description"],
            destination_type = rtRule["destination_type"]
            )
        )
    try:
        create_route_table_response = core_client.create_route_table(
            create_route_table_details=oci.core.models.CreateRouteTableDetails(
                compartment_id=rtconfig["routeTableConfig"]["compartment_id"],
                route_rules=rtRulesAry,
                vcn_id=rtconfig["routeTableConfig"]["vcn_id"],
                display_name=rtconfig["routeTableConfig"]["display_name"],
                defined_tags=defined_tags if defined_tags else None,
                freeform_tags=freeform_tags if freeform_tags else None,
            ))
        if create_route_table_response.status != 200:
            print("> ERROR: exception creation route table!  Response:")
            print("{}".format(create_route_table_response.data))
            raise
        else:
            rt_id = create_route_table_response.data.id
            print("Route table created...." + str(rt_id))
            return rt_id
    except oci.exceptions.ServiceError as e:
        print("! ERROR: executing the API call:")
        print(e)

##### Function to create VLAN ########
def create_vlan(core_client, vlconfig, freeform_tags, defined_tags):
    # Create a DRG
    print("Creating VLAN \"{}\"...".format(vlconfig["display_name"]))
    try:
        create_vlan_response = core_client.create_vlan(
            create_vlan_details=oci.core.models.CreateVlanDetails(
                cidr_block=vlconfig["cidr_block"],
                availability_domain=vlconfig["availability_domain"],
                compartment_id=vlconfig["compartment_id"],
                vcn_id=vlconfig["vcn_id"],
                display_name=vlconfig["display_name"],
                nsg_ids=vlconfig["nsg_ids"],
                route_table_id=vlconfig["route_table_id"],
                vlan_tag=vlconfig["vlan_tag"],
                freeform_tags=freeform_tags if freeform_tags else None,
                defined_tags=defined_tags if defined_tags else None
            )
        )
        if create_vlan_response.status != 200:
            print("> ERROR: exception creation VLAN!  Response:")
            print("{}".format(create_vlan_response.data))
            raise
        else:
            vlan_ocid = create_vlan_response.data.id
            print("VLAN created...." + str(vlan_ocid))
            return vlan_ocid
    except oci.exceptions.ServiceError as e:
        print("! ERROR: executing the API call:")
        print(e)

######### Function to attach a VNIC Details ###################
def attach_vnic (compute_client,vnicConf,instance_id):
    vnicids = []
    try:
        #Attach the VLAN to Physical nic 0 
        print("Attaching "+ str (vnicConf["display_name"]) + " to Nic0")
        attach_vnic_response = compute_client.attach_vnic(
            attach_vnic_details=oci.core.models.AttachVnicDetails(
                create_vnic_details=oci.core.models.CreateVnicDetails(
                    display_name=vnicConf["display_name"] + ".nic0",
                    vlan_id=vnicConf["vlan_id"]),
                instance_id=instance_id,
                nic_index=0)
                )
        # Check the vnic attachment status and proceed after the 1st attachment is complete 
        i = 1
        get_vnic_attachment_response = compute_client.get_vnic_attachment(
            vnic_attachment_id=attach_vnic_response.data.id)

        while get_vnic_attachment_response.data.lifecycle_state != "ATTACHED" and i < 300:
            get_vnic_attachment_response = compute_client.get_vnic_attachment(
                vnic_attachment_id=attach_vnic_response.data.id)
            print("Lifecycle state of vnic 0: "+ str(get_vnic_attachment_response.data.lifecycle_state))
            i += 1
            time.sleep(2)

        vnic_ocid = attach_vnic_response.data.id
        print("vNIC attached to Physical nic 0 ...." + str(vnic_ocid))
        print(get_vnic_attachment_response.data)
        vnicids.append(vnic_ocid)

        print("\n\nTaking a quick 10s nap......\n\n")
        time.sleep(10)

        #Attach the VLAN to Physical nic 1 
        print("Attaching "+ str (vnicConf["display_name"]) + " to Nic1")
        attach_vnic_response = compute_client.attach_vnic(
            attach_vnic_details=oci.core.models.AttachVnicDetails(
                create_vnic_details=oci.core.models.CreateVnicDetails(
                    display_name=vnicConf["display_name"] + ".nic1",
                    vlan_id=vnicConf["vlan_id"]),
                instance_id=instance_id,
                nic_index=1)
                )
        
        # Check the vnic attachment status and proceed after the 2nd attachment is complete 
        j = 1
        get_vnic_attachment_response1 = compute_client.get_vnic_attachment(
            vnic_attachment_id=attach_vnic_response.data.id)

        while get_vnic_attachment_response1.data.lifecycle_state != "ATTACHED" and j < 300:
            get_vnic_attachment_response1 = compute_client.get_vnic_attachment(
                vnic_attachment_id=attach_vnic_response.data.id)
            # Get the data from response
            print("Lifecycle state of vnic 1: "+ str(get_vnic_attachment_response1.data.lifecycle_state))
            j += 1
            time.sleep(2)

        print("vNIC attached to Physical nic 1 ...." + str(get_vnic_attachment_response1.data.id))
        print(get_vnic_attachment_response1.data)

    except oci.exceptions.ServiceError as e:
        print("! ERROR: executing the API call:")
        print(e)

def getInstanceOCIDs (ocvp_client, sddc_id):
    esxAry = []  
    try:
        # Send the request to ESXi service
        list_esxi_hosts_response = ocvp_client.list_esxi_hosts(
            sddc_id=sddc_id)

        # Loop through the ESXi hosts and push the esxi compute instance OCID to an array
        for item in list_esxi_hosts_response.data.items:
            get_esxi_host_response = ocvp_client.get_esxi_host(
                esxi_host_id=item.id
                )
            esxAry.append(get_esxi_host_response.data.compute_instance_id)
            
        return  esxAry
    except oci.exceptions.ServiceError as e:
        print("! ERROR: executing the API call:")
        print(e)

################Create a route table for VLANs####################
print("\n************** Create route table  ************************\n")
if (not data["routetable_id"]):
    routetable_id = create_rt_table(core_client,data["route-table-1"], None, None)
    data["route-table-1"]["routeTableConfig"]["route_table_id"] = routetable_id
else :
    routetable_id = data["routetable_id"]


###################  Create VLANS  #############################################
print("\n************** Create VLANS start ************************")

vlanOCIDs = []
for x in data["vlanConfig"]:
    x["route_table_id"] = routetable_id
    x["availability_domain"] = None
    x["vlan_tag"] =  None
    vlan_ocid = create_vlan(core_client, x, None, None)
    x["vlan_ocid"] = vlan_ocid
    vlanOCIDs.append(vlan_ocid)


#########  GET ESXi Hosts ####################
ocvp_client = oci.ocvp.EsxiHostClient(config)
esxAry = getInstanceOCIDs(ocvp_client,data["sddc_id"])


############ Attach VLAN to Vnic ###############
print("************** Attach VLANS start ************************")

for x in esxAry:
    for vlanOCID in vlanOCIDs:
        get_vlan_response = core_client.get_vlan(
            vlan_id=vlanOCID,
        )
        dName = get_vlan_response.data.display_name
        dName = dName.split("-",3)
        dName = dName[3].lower()
        attachVnicConfig = {
            "display_name":dName,
            "vlan_id":get_vlan_response.data.id
        }
        print("Attaching VLAN " + str(get_vlan_response.data.display_name)+ " to ESXi: "+ str(x))
        attach_vnic (core_compute_client,attachVnicConfig,x)


print("************** The script completed successfully ************************\n")

#calculate the execution time
end = datetime.now()
print("The time of execution of above program is :",
      str(end-start)[5:])
