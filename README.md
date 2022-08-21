# ocvs-vlan
Project : 
Oracle Cloud VMware Service (OCVS) allows for adding additional VLANS to the bare metal ESXi instances. However, creating those VLANS and attaching the VLANS to the 2 physical nics of the server is a time consuming process. This automation will automatically create the route table, route rules, VLANS and Attach those VLANS to the both ESXi host physical nics. 

Installation : 
Uopdat the sample inputs.json file and pass it to the script. 

Usage : 
Execute the python script after passing the inputs.json file. The user can specify an existing route table as well. 

Contributing : 
Fork it!
Create your feature branch: git checkout -b my-new-feature
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin my-new-feature
Submit a pull request :D

Credits : 
James George (Oracle)

License : 
Open Source MIT License