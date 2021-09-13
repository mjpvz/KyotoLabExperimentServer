# labExperimentKyoto

Step 1 through 9 are one time. Step 10 onwards need to be done for each experiment.

Setup an AMT requester account
1) https://requester.mturk.com/

When created link it to an AWS account. (AMT is a service under the AWS umbrella, but you can in theory use it without making an AWS account. Now we need it)
1) On https://requester.mturk.com/, go 'Developer' 
2) Follow the Step1 to create an AWS account
3) Link your AWS and AMT account in Step2. Be sure to copy your ACCESS KEY ID and SECRET ACCES KEY
4) register for a mturk sandbox account

5) On the server, make sure you have a personal user account.

6) On the server, run the following command to enter the virtual enviroment
   	source /home/labExperiment/labExperimentEnv/bin/activate
8) Now add the ADD_YOUR_NAME_HERE in your bashrc file
	nano ~/.bashrc
	go all the way to the bottom of the file and add the following
    
        AMT_BOTO_PROFILE="ADD_YOUR_NAME_HERE"; export AMT_BOTO_PROFILE
        alias lab='source /home/labExperiment/labExperimentEnv/bin/activate'
        alias labCelery='celery -A labExperiment worker -l INFO'

    save the file and reload your ssh window ( source ~/.bashrc) 

7) Start the AWS configuration by running the following command
   aws configure --profile ADD_YOUR_NAME_HERE
9) Follow the propts by entering the ACCES KEY ID and SECRET ACCESS KEY. For Region name choose us-east-1, default output can be left blank
	Now, every time you run any code that makes connection with AMT it will use your AWS configuration on the server and thus your AWS account. 

10) Make sure that Celery is running in an tmux window
    First, see all open tmux windows
        tmux ls
    If this returns 'Celery: ....' then that means there's already a tmux window open. 
    Attach to that tmux window
        tmux attach -t Celery
    If no tmux celery window was open before, make a new one
        tmux new -s Celery
    You will now be attached to the tmux celery window (either by joining it or by making a new one)
    In the celery window, make sure we are connected to the labExperiment virtual enviromnet (step 6)
    Then, run Celery
        celery -A labExperiment worker -l INFO
    You can now exit tmux by 
        ctrl+b d

11) To create a new experiment. First make sure you're in the virtual enviroment (step 6)
        cd /home/labExperiment
        ./manage.py create_new_experiment --experiment YOUR_EXP_NAME_HERE

12) For this experiment, make a new instance of that experiment.
        cd /home/labExperiment
        ./manage.py create_new_experiment_instance --experiment YOUR_EXP_NAME_HERE --experiment_instance YOUR_EXP_INSTANCE_NAME_HERE
    If you want to change settings for this version, change them in config.json. If you want to change them after running the experiment, better to create a new experiment instance

13) This will have created a a .html, .js and a .css file within the 'files' folder.
	Change the files to reflect your experiment
	After making changes execute the "./manage.py reload" command from the /home/webExperiment folder so the server will be updated

14) You can test your experiment (not through AMT) by going to 
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/0/
    Note that the last part of the url (/0/) indicates the condition. If you have multiple conditions, you can see the next conditions like so...
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/1/
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/2/ ..etc

    
15) Once everything is working as intended launch your experiment to SANDBOX
    make sure "MTURK_SANDBOX" in /home/webExperiment/settings.py is "True"

16) submit to AMT sandbox: 
    ./manage.py execute_experiment --experiment EXPERIMENT_NAME --experiment_instance EXPERIMENT_INSTANCE_NAME


17) test everything, submit data. Are your functions and html working properly?

18) If yes, change  MTURK_SANDBOX to False in labExperiment.settings

19) Run the ./manage execute again as in step 17