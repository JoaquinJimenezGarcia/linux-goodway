#!/usr/bin/env bash
http_ok() { [[ "$1" == "200" ]] && echo yes || echo no; }
http_redirect() { [[ "$1" == "301" || "$1" == "302" ]] && echo yes || echo no; }
