from uuid import getnode as get_mac


mac_add = get_mac()

print(hex(mac_add))