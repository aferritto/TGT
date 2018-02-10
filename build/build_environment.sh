#!/usr/bin/env bash

install_conda() {
  rm -rf $HOME/miniconda
  bash $HOME/miniconda.sh -b -p $HOME/miniconda

  if [[ ":$PATH:" != *":$HOME/miniconda/bin:"* ]]; then
    export PATH="$HOME/miniconda/bin:$PATH"
  fi
}

# arg 1 is "new" for new env, "update" for updating env
create_environment() {
    if [[ $1 == "update" ]]; then
      conda env update --prune -v -f environment.yml
    elif [[ $1 == "new" ]]; then
      conda env create -v -f environment.yml
    else
      >&2 echo "Error: arg 1 must be "new" or "update""
      exit 1
    fi
}

###############################################################################################

wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $HOME/downloads/miniconda.sh

# Create copies of files is non-existent
if [ ! -f $HOME/cached/environment.yml ]; then
    cp environment.yml $HOME/cached/environment.yml
fi

if [ ! -f $HOME/cached/miniconda.sh ]; then
    cp $HOME/downloads/miniconda.sh $HOME/cached/miniconda.sh
fi


# Look for changes and update accordingly
if ! cmp -s miniconda.sh cached/miniconda.sh; then
  install_conda
  create_environment "new"
elif ! cmp -s environment.yml cached/environment.yml; then
  create_environment "update"
fi