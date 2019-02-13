import argparse
import json
import subprocess
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--region', required=True)
args = parser.parse_args()

def get_active_branches():
    resp = urllib.request.urlopen("https://api.github.com/repos/hitta-skyddsrum/services/branches")
    if resp.getcode() != 200:
        raise Exception("Couldn't get branches from GitHub. HTTP status: {}. Body: {}".format(resp.getcode(), resp.read()))

    resp_json = json.loads(resp.read())
    return list(map(lambda b: b['name'], resp_json))

def get_aws_cmd_stdout(cmd):
    cmd.extend(["--region", args.region])
    ex = subprocess.run(cmd, capture_output=True)

    if ex.returncode != 0:
        raise Exception("{} failed with {}".format(' '.join(cmd), ex.stderr))

    return ex.stdout

def get_functions_with_tag(tag):
    json_output = json.loads(get_aws_cmd_stdout(["aws", "lambda", "list-functions"]))
    fns = []

    for fn in json_output['Functions']:
        json_fn = json.loads(get_aws_cmd_stdout(["aws", "lambda", "get-function", "--function-name", fn['FunctionName']]))

        if 'Tags' in json_fn and 'project' in json_fn['Tags'] and json_fn['Tags']['project'] == tag:
            fns.append(fn)

    return fns

def get_stale_aws_fns(fns, branches):
    return list(filter(lambda f: f in branches == False, fns))

print("Fetching active branches...")
active_branches = get_active_branches()
print("Found {} active branches:".format(len(active_branches)))
for branch in active_branches:
    print("* {}".format(branch))
print("")

aws_tag = "hitta-skyddsrum-services"
print("Fetching Lambda functions with tag {}...".format(aws_tag))
aws_fns = get_functions_with_tag(aws_tag)
print("Found {} Lambda functions with tag {}:".format(len(aws_fns), aws_tag))
for fn in aws_fns:
    print("* {}". format(fn['FunctionName']))

stale_aws_fns = get_stale_aws_fns(aws_fns, active_branches)
print("Found {} stale Lambda functions:".format(len(stale_aws_fns)))
for fn in stale_aws_fns:
    print("* {}". format(fn['FunctionName']))
print("")
