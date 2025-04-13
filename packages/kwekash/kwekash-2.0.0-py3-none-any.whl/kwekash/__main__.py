#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import shutil

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run weka commands inside a WEKA drive pod in Kubernetes."
    )
    parser.add_argument("--kubeconfig", help="Path to kubeconfig file", default=os.environ.get("KUBECONFIG"))
    parser.add_argument("--namespace", help="Kubernetes namespace", default="weka-operator-system")
    parser.add_argument("--pod-match", help="Substring to match in pod name", default="drive")
    parser.add_argument("-it", action="store_true", help="Open an interactive shell")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to pass to weka or watch")
    return parser.parse_args()

def run_cmd(command, shell=False):
    print("🔧 Running:", " ".join(command) if isinstance(command, list) else command)
    subprocess.run(command, check=False, shell=shell)

def main():
    args = parse_args()

    if not args.kubeconfig:
        print("❌ Error: --kubeconfig must be set or $KUBECONFIG must be defined.")
        sys.exit(1)

    kubecmd = "kubecolor" if shutil.which("kubecolor") else "kubectl"
    base_cmd = [kubecmd, "--kubeconfig", args.kubeconfig, "-n", args.namespace]

    try:
        pod_list = subprocess.check_output(base_cmd + ["get", "pods"]).decode().splitlines()
        pod_name = next(line.split()[0] for line in pod_list if args.pod_match in line)
    except StopIteration:
        print(f"❌ Error: No pod found matching '{args.pod_match}' in namespace '{args.namespace}'")
        sys.exit(1)

    print(f"🔍 Using pod: {pod_name} in namespace: {args.namespace}")
    print(f"📁 Using kubeconfig: {args.kubeconfig}")

    if args.it:
        run_cmd(base_cmd + ["exec", "-it", pod_name, "--", "bash"])
    elif args.cmd and args.cmd[0] == "watch":
        watch_opts = []
        weka_args = []
        for arg in args.cmd[1:]:
            (watch_opts if arg.startswith("-") else weka_args).append(arg)
        run_cmd(base_cmd + ["exec", "-it", pod_name, "--", "watch"] + watch_opts + ["weka"] + weka_args)
    elif not args.cmd:
        run_cmd(base_cmd + ["exec", pod_name, "--", "weka", "status"])
    else:
        run_cmd(base_cmd + ["exec", pod_name, "--", "weka"] + args.cmd)

if __name__ == "__main__":
    main()
