#!/bin/sh

# Runs clone_all.sh with defaults, designed to be user editable

# Written By: Brian Konzman

if [[ ("${#}" -ne "2") && ("${#}" -ne "3") ]];
	then
	echo ""
	echo "This script is designed to be edited by the user and will run clone_all.sh with defaults"
	echo ""
	echo "Please provide 2 parameters:"
	echo "1. Your github account name"
	echo "2. The unique identifier of the specific assignment, usually it means the prefix, e.g. lab2-partA"
	echo "(optional) 3. Additional command after cloning a repo; we already cd into the repo for you."
else

	assignment=$2
	additional_commands=${3:-":"}

	#edit these variables to your defaults
	organization="SI669-classroom"
	username=$1
	protocol="https"

	source ./clone_all.sh ${organization} ${assignment} ${username} ${protocol} ${additional_commands}
fi
