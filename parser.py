#!/usr/bin/env python3
import subprocess

result = subprocess.run(["ps",
                         "axo",
                         "user:20,pcpu,rss,comm:20",
                         "--sort", "-%cpu",
                         "--no-heading"], capture_output=True)
output = result.stdout.decode("utf-8")
list_of_prc = [i.split() for i in output.split("\n")]
list_of_prc.pop()  #remove empty item at the end

'''
join process names that contain of more than one word
since we set output to 4 columns only, 4+ columns are parts of name of process
'''
for i in list_of_prc:
    while len(i) > 4:
        i[len(i)-2] += f" {i.pop()}"

'''
gathers info about users, total cpu and mem usage
'''
prc_users = {}
total_cpu = 0
total_mem = 0
for i in list_of_prc:
    if i[0] in prc_users.keys():
        prc_users[i[0]] += 1
    else:
        prc_users[i[0]] = 1
    total_cpu += float(i[1])
    total_mem += float(i[2])

'''
Creates a string with listed user and amount of his processes. Each user on new line. Sorted by descending order
'''
processes_per_user = "\r\n".join([f"{i[0]}: {i[1]}" for i in sorted(prc_users.items(),
                                                                    key=lambda x: x[1], reverse=True)])
total_processes = len(list_of_prc)
total_mem_mb = total_mem/1000
'''
Creates a string of all users with processes separated by comma
'''
system_users = ", ".join([i for i in prc_users.keys()])

print(f"~~ System Users: {system_users} ~~")
print(f"~~ Total running processes: {total_processes} ~~")
print(f"~~ Processes per user:\r\n{processes_per_user }")
print(f"~~ Total Memory in use = {'%.2f'%total_mem_mb}Mb ~~")
print(f"~~ Total CPU in use = {'%.2f'%total_cpu}% ~~")
print(f"~~ Most CPU is used by: {list_of_prc[0][3]}")
print(f"~~ Most MEM is used by: {sorted(list_of_prc, key=lambda x: x[2], reverse=True)[0][3]}")


