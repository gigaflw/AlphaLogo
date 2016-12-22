## How to use github

#### use with command line

##### Installation
1. Windows

	Download [git bash](https://git-for-windows.github.io/)

2. Mac

	install with homebrew
	
		ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
		brew install git

3. Linux
	
	do it yourself

##### Basic commands

A simple workflow

	git clone <remote_repository_name> <local_directory_name>
	// get codes

	..do something to the codes
	
	git pull
	// pull down your teammates' change
	
	git add -A 
	// save changes to git cache, '-A' means save all the changes
	
	git commit -m "My first commit"
	// commit changes to git local repository
	// now your changes can be seen in the commit history
	// summary your changes
	
	git push
	// now changes have been pushed to github
	// can be shared by your teammates

Hints
	
	git status
	// your will see your files' status
	git diff
	// show changes that not saved yet
	git history
	// show commit history
	

#### use with descktop

##### Installation

Download from [here](https://desktop.github.com/)

##### Usage

Click the 'sync' button!!!!!! 



[More tutorial](http://rogerdudler.github.io/git-guide/index.zh.html)
