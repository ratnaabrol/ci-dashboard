#!/bin/bash

## default values
path=$(cat /etc/ci-dashboard.config)
host=${host:-127.0.0.1}
port=${port:-5000}

help() {

    echo "CI-Dashboard help
    Options:
    start :        start the server.
        options:
        --host : the hostname to listen on, default 127.0.0.1
        --port : the port of the webserver, default 5000
    stop   :    stop the server.
    update :    update software.
    "
}

startServer() {

    if tmux new -d -s cidashboard python3 ${path}/ci-dashboard/main.py --host ${host} --port ${port} ; then
        sleep 2
        if curl -I http://${host}:${port} &> /dev/null; then
            echo "CI-Dashboard server is started in tmux session [cidashboard].
            Server url : http://${host}:${port}
            Note: to open the session type 'tmux a -t cidashboard' in the terminal."
        else
            echo "Can't start CI-Dashboard server"; exit 1
        fi
    else
        echo "Can't start CI-Dashboard server"; exit 1
    fi
}

stopRunningServer() {
    if tmux kill-session -t cidashboard &> /dev/null; then
        echo "CI-Dashboard server is stopped"
    else
        echo "Can't stop CI-Dashboard server"; exit 1
    fi
}

updateSoftware() {
    if git -C ${path}/ci-dashboard/ pull ; then
        echo "CI-Dashboard server is updated"
    else
        echo "Can't update CI-Dashboard"; exit 1
    fi
}

command=$1
shift

if [ -z ${command} ]; then
    echo "Error: Missing command"
    help

elif [ ${command} == 'help' ]; then
    help

elif [ ${command} == 'start' ]; then
    while true; do
        case "$1" in
            -h | --host ) host="$2"; shift 2;;
            -p | --port ) port="$2"; shift 2;;
            -- ) shift; break ;;
            -* ) echo "Unrecognized option $1"; exit 1;;
            * ) break;;
        esac
    done
    startServer 

elif [ ${command} == 'stop' ]; then
    stopRunningServer

elif [ ${command} == 'update' ]; then
    updateSoftware
else
    echo "Error: Unrecognized command"
    help
fi
