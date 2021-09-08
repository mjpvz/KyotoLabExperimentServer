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
        save the file and reload your ssh window ( source ~/.bashrc) 
7) Start the AWS configuration by running the following command
   aws configure --profile ADD_YOUR_NAME_HERE
9) Follow the propts by entering the ACCES KEY ID and SECRET ACCESS KEY. For Region name choose us-east-1, default output can be left blank
	Now, every time you run any code that makes connection with AMT it will use your AWS configuration on the server and thus your AWS account. 




10) To create a new experiment 
    cd /home/labExperiment
    ./manage.py create_new_experiment

11) This command will have created a number of new folders for your experiment

12) For this experiment, make a new version of that experiment
    cd /home/labExperiment/experiments/current/YOUR_EXPERIMENT_NAME_HERE/create_new_experiment_instance.py
    If you want to change settings for this version, change them in config.json. If you want to change them after running the experiment, better to create a new experiment

13) This will have created a number of files within the 'files' folder.
	Change the files to reflect your experiment
	To see a change on the server execute the "./manage.py reload" command from the /home/webExperiment folder

14) You can test your experiment (not through AMT) by going to 
	http://133.3.249.99/experiments/EXPERIMENT_NAME/EXPERIMENT_INSTANCE_NAME/

15) launch your experiment to SANDBOX
    make sure "MTURK_SANDBOX" in /home/webExperiment/settings.py is "True"

16) submit to AMT sandbox: 
    ./manage.py execute_experiment --experiment EXPERIMENT_NAME --experiment_instance EXPERIMENT_INSTANCE_NAME
