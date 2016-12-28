#!/bin/bash

pip_path=$1
declare -a PKG_LEAF=()
declare -a PKG_DEPS=()

if [ -z $1 ]; then
    echo $"Use: $0 {pip_path}, where pip_path could be something like /bin"
    exit -1
fi

# List all packages installed 
PKGS=`${pip_path}/pip --disable-pip-version-check list | awk '{print $1}'`

# Now store packages that are dependency of others
for i in $PKGS; do
    RQR=`${pip_path}/pip show $i | grep Requires: | awk -F : '{print $2}'`
    echo "Package: $i, dependencies: $RQR"
    IFS=',' read -ra PKG <<< "$RQR"
    for j in "${PKG[@]}"; do
        if [[ " ${PKG_DEPS[*]} " != *" $j "* ]]; then
            PKG_DEPS=("${PKG_DEPS[@]}" "$j")
        fi
    done
done

# Leaf packages 
for i in $PKGS; do
    if [[ " ${PKG_DEPS[*]} " != *" $i "* ]]; then
        PKG_LEAF=("${PKG_LEAF[@]}" "$i")
    fi
done

echo ""
echo "Packages installed:"
echo $PKGS
echo ""
echo "Packages installed because it is a dependency:"
echo ${PKG_DEPS[@]}
echo ""
echo "Leaf packages:"
echo ${PKG_LEAF[@]}
