import re
nic_number = "inside_real_host_insvr_adsvr_172.18.10.20 (2)"
s = re.sub(' ', '_', nic_number)
s = re.sub('(2)','1',s)
s = s[:-3]
s = s+"1"

print(s)