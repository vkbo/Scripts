#!/bin/bash

cd /opt
sudo rm -rf firefox.old
sudo mv firefox firefox.old
sudo tar -xvf $1

