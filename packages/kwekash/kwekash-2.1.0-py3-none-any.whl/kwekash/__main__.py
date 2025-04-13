#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import shutil
import configparser
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Run weka commands inside a WEKA drive pod in Kubernetes.")
    parser.add_argument("--kubeconfig", help="Path to kubeconfig file", default=None)
    parser.add_argument("--namespace", help="Kubernetes namespace", default=None)
    parser.add_argument("--pod-match", "-p", help="Substring to match in pod name", default=None)
    parser.add_argument("-it", action="store_true", help="Open an interactive shell")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to pass to weka or watch")
    return parser.parse_args()

def load_config():
    config = configparser.ConfigParser()
    config_path = Path.home() / ".config" / "kwekash" / "config.ini"
    if config_path.exists():
        config.read(config_path)
        return config["kwekash"]
    return {}

def run_cmd(command, shell=False):
    print("🔧 Running:", " ".join(command) if isinstance(command, list) else command)
    subprocess.run(command, check=False, shell=shell)

def main():
    config = load_config()
    args = parse_args()

    kubeconfig = args.kubeconfig or os.environ.get("KUBECONFIG") or config.get("kubeconfig")
    namespace = args.namespace or config.get("namespace", "weka-operator-system")
    pod_match = args.pod_match or config.get("pod_match", "drive")

    if not kubeconfig:
        print("❌ Error: --kubeconfig must be set, or $KUBECONFIG, or config file.")
        sys.exit(1)

    kubecmd = "kubecolor" if shutil.which("kubecolor") else "kubectl"
    base_cmd = [kubecmd, "--kubeconfig", kubeconfig, "-n", namespace]

    try:
        pod_list = subprocess.check_output(base_cmd + ["get", "pods"]).decode().splitlines()
        pod_name = next(line.split()[0] for line in pod_list if pod_match in line)
    except StopIteration:
        print(f"❌ Error: No pod found matching '{pod_match}' in namespace '{namespace}'")
        sys.exit(1)

    print(f"🔍 Using pod: {pod_name} in namespace: {namespace}")
    print(f"📁 Using kubeconfig: {kubeconfig}")

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
