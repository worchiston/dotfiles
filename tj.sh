#!/bin/bash
# tj (tinyjournal)
# Journaling application that is basically a wrapper around vim and less

tj_p() {
    export TJ_PATH=$1
}

tjcd() {
    cd $TJ_PATH
}

tjne() {
    vim $(date --iso-8601=seconds).md
}

tjve() {
    ls | sort -r | xargs less
}

tjse() {
    echo "$@"
    grep -iR "$@"
}
