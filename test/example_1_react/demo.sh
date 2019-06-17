#!bin/bash

########################## [LIBRARY]

# tinylogger.bash - A simple logging framework for Bash scripts in < 10 lines
# https://github.com/nk412/tinylogger

# Copyright (c) 2017 Nagarjuna Kumarappan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author: Nagarjuna Kumarappan <nagarjuna.412@gmail.com>

# defaults
LOGGER_FMT=${LOGGER_FMT:="%Y-%m-%d %H:%M:%S"}
LOGGER_LVL=${LOGGER_LVL:="info"}

function tlog() {
    action=$1 && shift
    case $action in
    debug) [[ $LOGGER_LVL =~ debug ]] && echo "$(date "+${LOGGER_FMT}") - DEBUG - $@" 1>&2 ;;
    info) [[ $LOGGER_LVL =~ debug|info ]] && echo "$(date "+${LOGGER_FMT}") - INFO  - $@" 1>&2 ;;
    warn) [[ $LOGGER_LVL =~ debug|info|warn ]] && echo "$(date "+${LOGGER_FMT}") - WARN  - $@" 1>&2 ;;
    error) [[ ! $LOGGER_LVL =~ none ]] && echo "$(date "+${LOGGER_FMT}") - ERROR - $@" 1>&2 ;;
    esac
    true
}

##########################

get_os() {
    tlog debug "Checking OS..."

    # https://stackoverflow.com/questions/3466166/how-to-check-if-running-in-cygwin-mac-or-linux
    unameOut="$(uname -s)"
    local machine=""
    case "${unameOut}" in
    Linux*) machine=Linux ;;
    Darwin*) machine=Mac ;;
    CYGWIN*) machine=Cygwin ;;
    MINGW*) machine=MinGw ;;
    *) machine="UNKNOWN:${unameOut}" ;;
    esac

    tlog debug "Checking OS... [DONE]"
    echo "$machine"
}

_start_docker_daemon_mac() {
    tlog debug "Starting Docker Daemon on Mac..."

    # https://forums.docker.com/t/restart-docker-from-command-line/9420/8
    tlog debug "Open Docker App..."
    open --background -a Docker

    tlog debug "Checking Docker App Ready Status..."
    while ! docker system info >/dev/null 2>&1; do sleep 1; done

    tlog debug "Starting Docker Daemon on Mac...[DONE]"
}

start_docker_daemon() {
    tlog debug "Starting Docker Daemon..."
    case "$1" in
    Mac*)
        _start_docker_daemon_mac
        ;;
    *)
        echo "Error! OS is not supported to start docker" 1>&2
        exit 500
        ;;
    esac
    tlog debug "Starting Docker Daemon...[DONE]"
}

_run_backend_image() {
    local CONTAINER_NAME=${CONTAINER_NAME:="abs-backend"}
    tlog debug "Running $CONTAINER_NAME container..."
    # run image
    dumpInfo="$(docker start $CONTAINER_NAME 2>&1)"

    if [[ $dumpInfo == *"No such container:"* ]]; then
        tlog warn "No '$CONTAINER_NAME' container found in docker"
        exit 1
    fi

    tlog debug "Running $CONTAINER_NAME container...[DONE]"
}

_build_backend_image() {
    tlog debug "Deploying abs-backend image..."

    local DIR_BACKEND_IMAGE=${DIR_BACKEND_IMAGE:="/Users/affandhia/Documents/Affan/skripsi/abs-backend/backend-image"}
    local CONFIG_BACKEND_IMAGE_EMAIL=${CONFIG_BACKEND_IMAGE_EMAIL:="spicervolt@gmail.com"}
    local CONFIG_BACKEND_CONTAINER_NAME=${CONFIG_BACKEND_CONTAINER_NAME:="spicervolt@gmail.com"}
    local return_dir="$(pwd)"

    tlog debug "Changing working dir to $DIR_BACKEND_IMAGE..."
    cd $DIR_BACKEND_IMAGE

    tlog debug "Passing email name..."
    export EMAIL=$CONFIG_BACKEND_IMAGE_EMAIL
    export BACKEND_CONTAINER_NAME=$CONFIG_BACKEND_CONTAINER_NAME

    tlog debug "Running build image script..."
    bash "$DIR_BACKEND_IMAGE/build.sh"

    tlog debug "Returning working dir to $return_dir..."
    cd $return_dir

    tlog debug "Deploying abs-backend image...[DONE]"
}

_start_backend_mac() {
    (
        # try catch solution: https://stackoverflow.com/questions/34096777/how-to-throw-an-error-in-bash

        # running inside subshell by using "()"
        _run_backend_image
    ) || {
        # catch container not found
        # TODO: build image
        _build_backend_image
    }
}

start_backend() {
    case "$1" in
    Mac*)
        _start_backend_mac
        ;;
    *)
        echo "Error! OS is not supported to start backend " 1>&2
        exit 501
        ;;
    esac
}

run_ui_generator() {
    tlog debug "Running UI Generator..."

    local DIR_UI_GENERATOR=${DIR_UI_GENERATOR:="/Users/affandhia/Documents/Affan/skripsi/ifml-angular-pwa/test/example_1_react"}
    local return_dir="$(pwd)"

    tlog debug "Changing working dir to $DIR_UI_GENERATOR..."
    cd $DIR_UI_GENERATOR

    tlog debug "Running UI Generator script..."
    # only in certaine device
    if [[ "$(uname -a)" == *"Affan-Macbook-Pro.local"* ]]; then
        tlog debug "Running UI Generator script on Affan-Macbook-Pro.local..."
        /Users/affandhia/.pyenv/versions/anaconda3-5.1.0/envs/py36/bin/python __init__.py
    else
        echo "Error! Computer is not supported to start UI generator " 1>&2
        exit 502
    fi

    tlog debug "Returning working dir to $return_dir..."
    cd $return_dir

    tlog debug "Running UI Generator...[DONE]"
}

run_generated_web() {
    tlog debug "Running Generated Web..."

    local DIR_GENERATED_WEB=${DIR_GENERATED_WEB:="/Users/affandhia/Documents/Affan/skripsi/ifml-angular-pwa/test/example_1_react/result/abs-bankaccount"}
    local return_dir="$(pwd)"

    tlog debug "Changing working dir to $DIR_GENERATED_WEB..."
    cd $DIR_GENERATED_WEB

    tlog debug "Installing node_modules..."
    yarn
    tlog debug "Building generated web..."
    yarn build
    tlog debug "Running generated web in the background..."
    # https://spin.atomicobject.com/2017/08/24/start-stop-bash-background-process/
    trap "exit" INT TERM ERR
    trap "kill 0" EXIT

    yarn start:production &

    echo "$(jobs)"

    # open in Google Chrome
    if [[ "$(uname -a)" == *"Affan-Macbook-Pro.local"* ]]; then
        tlog debug "Opening localhost:3001 on Incognito Google Chrome in 5 seconds..."
        sleep 5
        open -na "Google Chrome" --args --incognito "http://localhost:3001"
        # STOPPING server (IF localhost:30001 always serving regardless the incognito has been closed and reopen)
        # lsof -n -i4TCP:3001
        # PID is second field. Then, kill that process:
        # kill -9 PID
    else
        echo "Error! Computer is not supported to open http://localhost:3001 in Google Crhome " 1>&2
        exit 503
    fi

    tlog debug "Returning working dir to $return_dir..."
    cd $return_dir

    tlog debug "Running Generated Web...[DONE]"
}

main() {
    # - make sure Docker is running ✅
    # - make sure environment is already set to anaconda3.x ✅
    # - deploy docker image OR run existing docker image ✅
    # - run test/example_1/__init__.py ✅
    # - run yarn in result/abs-bankaccount and prettier only in /src ✅
    # - open localhost:3000 automatically  ✅
    # - login with DEMO account affandhia@gmail.com (spicervolt@gmail.com HAS 2FA) DONT USE 2FA for time saving [✅ on DEMO]

    # CONFIG
    LOGGER_LVL="debug"
    CONTAINER_NAME="abs-backend"

    DIR_BACKEND_IMAGE="/Users/affandhia/Documents/Affan/skripsi/abs-backend/backend-image"
    CONFIG_BACKEND_IMAGE_EMAIL="affandhia@gmail.com"
    CONFIG_BACKEND_CONTAINER_NAME=$CONTAINER_NAME

    DIR_UI_GENERATOR="/Users/affandhia/Documents/Affan/skripsi/ifml-angular-pwa/test/example_1_react"

    DIR_GENERATED_WEB="$DIR_UI_GENERATOR/result/abs-bankaccount"
    # CONFIG [END]

    # check OS
    userOS="$(get_os)"
    tlog info "Operating System: $userOS"

    # start docker daemon
    start_docker_daemon "$userOS"
    tlog info "Docker Daemon has been started."

    # start backend image
    # backend image config
    start_backend "$userOS"
    tlog info "Backend $CONTAINER_NAME has been run."

    run_ui_generator
    tlog info "UI Generator has been run."

    run_generated_web
    tlog info "Generated web has been started on http://localhost:3001."

    tlog info "Logging web server output..."
    wait
}

main
