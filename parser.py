#!/usr/bin/env python3
import subprocess
import time

output = subprocess.run(["ps",
                         "axo",
                         "user:20,pcpu,rss,comm:20",
                         "--sort", "-%cpu",
                         "--no-heading"], capture_output=True). \
    stdout.decode("utf-8")
list_of_processes = [i.split() for i in output.split("\n")]
list_of_processes.pop()  # remove empty item at the end

'''
Parses list of entries, where every entry is list of columns data

Join process names that contain of more than one word
since we set output to 4 columns only, 4+ columns are parts of name of process

Counts: processes by username (0 item), total cpu (1st item) and mem usage(2nd item)

'''
prc_users = {}
total_cpu = 0
total_mem = 0

for i in list_of_processes:
    while len(i) > 4:
        i[len(i) - 2] += f" {i.pop()}"
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
total_processes = len(list_of_processes)  # Total amount of processes is len of list
total_mem_mb = total_mem / 1000  # Kb to MB conversion
system_users = ", ".join([i for i in prc_users.keys()])  # Combine info about users and processes into string

output_dict = {
    "System Users": f"{system_users}\r\n",
    "\r\nTotal running processes": f"{total_processes}\r\n",
    "\r\nProcesses per user": f"\r\n{processes_per_user}\r\n",
    "\r\nTotal Memory in use": f"{'%.2f' % total_mem_mb}Mb\r\n",
    "\r\nTotal CPU in use": f"{'%.2f' % total_cpu}%\r\n",
    "\r\nMost CPU is used by": f"{list_of_processes[0][3]}\r\n",
    "\r\nMost MEM is used by": f"{sorted(list_of_processes, key=lambda x: x[2], reverse=True)[0][3]}"
}

for i, j in output_dict.items():
    print(f"{i}: {j}", end='')

with open(f"{time.strftime('%d-%m-%y-%H:%M', time.localtime())}-stats.txt", "w") as out:
    for i, j in output_dict.items():
        out.write(f"{i}: {j}")
