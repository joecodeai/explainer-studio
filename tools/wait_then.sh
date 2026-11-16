#!/usr/bin/env bash
# wait until no process matches $1, then run the rest of the arguments
pat="$1"; shift
while pgrep -f "$pat" > /dev/null; do sleep 15; done
exec "$@"
