import re
import subprocess


def get_gateway_addr():
    result = subprocess.run(['ip', 'r'], capture_output=True)
    output = result.stdout.decode()
    # TODO: Handle exceptions
    return output.split('default via')[-1].split()[0]


def get_ip_addr():
    result = subprocess.run(['ip', 'r'], capture_output=True)
    output = result.stdout.decode()
    # TODO: Handle exceptions
    return output.split('src')[-1].split()[0]


def list_members_of_group(group_name):
    result = subprocess.run(['lid', '-g', group_name], capture_output=True)
    output = result.stdout.decode()
    splitted = re.split(r'\(([^()]+)\)\n', output)
    members = []
    for i in range(0, len(splitted) - 1, 2):
        members.append(splitted[i].strip())
    return members


if __name__ == '__main__':
    print('Default gateway address: ' + get_gateway_addr())
    print('IP address: ' + get_ip_addr())
