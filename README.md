# labExperimentKyoto

Step 1 through 9 only need to be done once. Step 10 onwards need to be done for each new experiment.

1) Setup an AMT requester account on https://requester.mturk.com/

When created, line your AMT requester account to an AWS account. (AMT is a service under the AWS umbrella, but you can in theory use it without 
making an AWS account. To use the developer mode, we need an aws account)

2) On https://requester.mturk.com/, go 'Developer' 
3) Follow the Step1 and onwards to create an AWS account
4) Link your AWS and AMT account in Step2. Be sure to copy your ACCESS KEY ID and SECRET ACCES KEY
5) register for a mturk sandbox account

6) On the server, run the following command to enter the virtual enviroment

   	<code> source /home/labExperiment/labExperimentEnv/bin/activate </code>
8) Now add the ADD_YOUR_NAME_HERE in your bashrc file

	<code> nano ~/.bashrc  </code>
	
	go all the way to the bottom of the file and add the following
    
        AMT_BOTO_PROFILE="ADD_YOUR_NAME_HERE"; export AMT_BOTO_PROFILE
        alias lab='source /home/labExperiment/labExperimentEnv/bin/activate'
        alias labCelery='celery -A labExperiment worker -l INFO'

    save the file and reload your ssh window ( source ~/.bashrc) 

7) Start the AWS configuration by running the following command

   	<code> aws configure --profile ADD_YOUR_NAME_HERE </code>
9) Follow the propts by entering the ACCES KEY ID and SECRET ACCESS KEY. For Region name choose us-east-1, default output can be left blank
	Now, every time you run any code that makes connection with AMT it will use your AWS configuration on the server and thus your AWS account. 

10) Make sure that Celery is running in an tmux window
    First, see all open tmux windows
        
   	<code> tmux ls </code>
   
   	If this returns 'Celery: ....' then that means there's already a tmux window open. 
Attach to that tmux window
                
   	<code> tmux attach -t Celery</code>
   
   	If no tmux celery window was open before, make a new one
                        
   	<code> tmux new -s Celery</code>
   
   	You will now be attached to the tmux celery window (either by joining it or by making a new one)
In the celery window, make sure we are connected to the labExperiment virtual enviromnet (step 6)
Then, run Celery
                        
   	<code> ./manage.py celery</code>
   
   	You can now exit tmux by 
                        
      <code>ctrl+b d</code>
   

11) To create a new experiment. First make sure you're in the virtual enviroment (step 6)
                                
      <code> cd /home/labExperiment</code>
                                
      <code> ./manage.py create_new_experiment --experiment YOUR_EXP_NAME_HERE</code>

12) For this experiment, make a new instance of that experiment.
                                        
      <code> cd /home/labExperiment</code>
                                        
      <code> ./manage.py create_new_experiment_instance --experiment YOUR_EXP_NAME_HERE --experiment_instance YOUR_EXP_INSTANCE_NAME_HERE </code>
	
      If you want to change settings for this version, change them in config.json. If you want to change them after running the experiment, better to create a new experiment instance

13) This will have created a a .html, .js and a .css file within the 'files' folder.
	Change the files to reflect your experiment. 
    In JS, Images can be accessed using the document.image_root variable. The condition can be accessed using the documnet.condition variable
	After making changes execute the "./manage.py reload" command from the /home/webExperiment folder so the server will be updated

14) You can test your experiment (not through AMT) by going to 

	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/0/
	
    Note that the last part of the url (/0/) indicates the condition. If you have multiple conditions, you can see the next conditions like so...
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/1/
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/2/ ..etc

    
15) Once everything is working as intended launch your experiment to SANDBOX
    make sure "MTURK_SANDBOX" in /home/webExperiment/settings.py is "True"

16) submit to AMT sandbox: 
                                            
      <code>./manage.py execute_experiment --experiment EXPERIMENT_NAME --experiment_instance EXPERIMENT_INSTANCE_NAME </code>
	


17) test everything, submit data. Are your functions and html working properly?

18) If yes, change  MTURK_SANDBOX to False in labExperiment.settings. This means that now the tasks will actually be submitted to mturk and not the sandbox

19) Repeat step 10, make sure that celery is running. Each change in code (except in .html, .css and, .js) will reload celery. If at any moment code is not valid, celery will fail. As such, make sure it is running. 

20) Run the ./manage execute again as in step 17
