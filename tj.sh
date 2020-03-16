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

# TODO: sort by newest first
tjve() {
    less *.md
}

tjse() {
    grep -iR $1
}