# MG2020
Object detection and machine learning algorithms for Ignite Refereeing 


## How to link up to github
(on pycharm but should work elsewhere)

Open up Terminal in python (one of the bottom tabs).
From the command line (e.g. $...) navigate to the folder you want to be in. e.g.:
```
    $ cd desired_folder
```
Clone the git repository:
```
    $ git clone https://github.com/rubix18/MG2020.git
```
You should see the MG2020 folder appear. Navigate into this folder:
```
    $ cd MG2020
```
(If this doesnt happen I might have missed something and you might need to do $ git pull)

Now check that your git connection is set up:
```
    $ git status
```
You should get something like this:
```
    (opencv_project) Becs-MBP:MG2020 bec$ git status
    On branch master
    Your branch is up to date with 'origin/master'.
    nothing to commit, working tree clean
```
You should also see in your PyCharm project tab the hello.txt and README.md files under the MG2020 folder

Now you can checkout the other branches:
```
    $ git checkout OpenCV
        OR
    $ git checkout SSD-Mobilenet
```
These should change the contents of your MG2020 folder to look like what is in the online github repository (just open
and close the folder in the Pycharm tab to refresh).

To create a new branch to work on your own code / add a new model you are going to want to check out a new branch:
```
    $ git checkout -b name_of_your_new_branch
```
You can check this worked by running:
```
    $ git status
```
Now create files or copy files in from your local directory to this folder. When you are ready to submit the changes you
have made to the repository run:
```
    $ git add -A
    $ git commit -m "Some message about this version of the code you are submiting"
    $ git push
```
Now when you check the status you should see:
```
    On branch SSD-Mobilenet
    Your branch is up to date with 'origin/SSD-Mobilenet'.
```
(For the name of your branch).
You should also now be able to navigate to this branch on the online git repository.

Lmk if none of this makes sense or I got something wrong. [-- By Bec]
