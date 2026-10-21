#!/usr/bin/env bash
avoid_docker_flag() { echo "--privileged"; }
prefer_cap_action() { echo drop; }
