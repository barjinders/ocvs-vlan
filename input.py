import json
from textwrap import indent
import oci



config = oci.config.from_file("~/.oci/configp", "DEFAULT")
# open the JSON file
f = open('/Users/barjindersingh/Documents/vrf-code/userInputs.json')
# parse the JSON file
try:
    data = json.load(f)
except json.decoder.JSONDecodeError:
    print("Invalid documentTemplate JSON")


""""
################Create a route table for VLANs####################
# Initialize service client with default config file
core_client = oci.core.VirtualNetworkClient(config)
routeTableConfig = {
    "compartment_id": compartment_ocvs,
    "network_entity_id": "ocid1.drg.oc1.ap-tokyo-1.aaaaaaaaedez2rcoq2y2pf23l4udlsw3cm52bs3vm22te5yel2js3m5bzodq",
    "destination": "0.0.0.0/0",
    "description": "Default route to OCI Firewall",
    "vcn_id": vcnId,
    "display_name": "Route Table for OCI Firewall traffic",
    "destination_type": "CIDR_BLOCK"
}

{
    "compartment_id": "ocid1.compartment.oc1..aaaaaaaawqa7l34gmt6jqxxxawkkbh7upnsn5bntrphfxocost6jm56pj3jq",
    "network_entity_id": "ocid1.drg.oc1.ap-tokyo-1.aaaaaaaaedez2rcoq2y2pf23l4udlsw3cm52bs3vm22te5yel2js3m5bzodq",
    "destination": "0.0.0.0/0",
    "description": "Default route to OCI Firewall",
    "vcn_id": "ocid1.vcn.oc1.ap-tokyo-1.amaaaaaap77apcqavoecdefbhzft6rab7ovqoizde76yo5giqbltlgjhgbua",
    "display_name": "Route Table for OCI Firewall traffic",
    "destination_type": "CIDR_BLOCK"
}

"""
route_table_id = "yyyyyyyyyyyy"
data["route-table-1"]["routeTableConfig"]["route_table_id"]  ="xxxxxxxxxxxxxxxxxxxxxx"

#print (json.dumps(data["route-table-1"], indent=4))

############### Create new VLANS #######################
vlanConfig = {
    # Gets the availability_domain of this CreateVlanDetails.
    "availability_domain":	None,
    # [Required] Gets the cidr_block of this CreateVlanDetails.
    "cidr_block": "10.1.38.0/29",
    # [Required] Gets the compartment_id of this CreateVlanDetails.
    "compartment_id": "compartment_ocvs",
    # Gets the display_name of this CreateVlanDetails.
    "display_name":	"VLAN-SDDC-JP-NSX Edge Uplink 3",
    # Gets the nsg_ids of this CreateVlanDetails.
    "nsg_ids":	["ocid1.networksecuritygroup.oc1.ap-tokyo-1.aaaaaaaa43vpe3tqiyirk7n3htsbvh5mln2nvrqsmfhz5zqsgvdeksvsc2sq"],
    # Gets the route_table_id of this CreateVlanDetails.
    "route_table_id": "routetable_id",
    "vcn_id":	"vcnId",  # [Required] Gets the vcn_id of this CreateVlanDetails.
    "vlan_tag": None  # Gets the vlan_tag of this CreateVlanDetails.
}
for x in data["vlanConfig"]:
    x["routetable_id"] = route_table_id
    #print (json.dumps(x,indent=4))



vlan_ocid= "ocid1.vlan.oc1.ap-tokyo-1.amaaaaaap77apcqalybtaowxpvmlucv35ydlubeq2x5cnwcscwxovma6kkkq"

# Initialize service client with default config file
core_client = oci.core.VirtualNetworkClient(config)


# Send the request to service, some parameters are not required, see API
# doc for more info
get_vlan_response = core_client.get_vlan(
    vlan_id=vlan_ocid,
)
dName = get_vlan_response.data.display_name
dName = dName.split("-",3)
dName = dName[3].lower()
print (dName) 
# Get the data from response
#print(get_vlan_response.data)