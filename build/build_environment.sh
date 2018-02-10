#!/usr/bin/env bash

conda_path() {
    export PATH="$HOME/miniconda/bin:$PATH"
}
install_conda() {
  rm -rf $HOME/miniconda
  bash $HOME/miniconda.sh -b -p $HOME/miniconda


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

echo "$PATH"

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
  echo "Rebuilding conda"
  install_conda
  conda_path
  echo "$PATH"
  create_environment "new"
elif ! cmp -s environment.yml cached/environment.yml; then
  echo "Rebuilding env"
  conda_path
  create_environment "update"
else
  conda "Using cached conda and env"
  conda_path
fi