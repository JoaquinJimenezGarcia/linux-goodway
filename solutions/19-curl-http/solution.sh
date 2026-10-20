#!/usr/bin/env bash
http_ok() { [[ "$1" == "200" ]] && echo yes || echo no; }
