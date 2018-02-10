#!/usr/bin/env bash

set_conda_path() {
    export PATH="$HOME/miniconda/bin:$PATH"
}
install_conda() {
  rm -rf $HOME/miniconda
  bash $HOME/downloads/miniconda.sh -b -p $HOME/miniconda
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
echo "Initial Path"
echo "$PATH"

wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $HOME/downloads/miniconda.sh

# Create copies of files is non-existent
if [ ! -f $HOME/cached/environment.yml ]; then
  echo "Creating cached copy of environment.yml"
  cp environment.yml $HOME/cached/environment.yml
fi

if [ ! -f $HOME/cached/miniconda.sh ]; then
  echo "Creating cached copy of miniconda.sh"
  cp $HOME/downloads/miniconda.sh $HOME/cached/miniconda.sh
fi

# Compare md5 sums of new and existing files
condaA=($(md5sum $HOME/downloads/miniconda.sh))
condaB=($(md5sum $HOME/cached/miniconda.sh))
envA=($(md5sum environment.yml))
envB=($(md5sum $HOME/cached/environment.yml))

if [[ $condaA != $condaB ]]; then
  echo "Rebuilding conda"
  install_conda
  set_conda_path
  create_environment "new"
elif [[ $envA != $envB ]]; then
  echo "Rebuilding env"
  set_conda_path
  create_environment "update"
else
  echo "Using cached conda and env"
  set_conda_path
fi

echo "Final PATH"
echo "$PATH"
