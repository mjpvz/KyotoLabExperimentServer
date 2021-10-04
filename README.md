# labExperimentKyoto

Step 1 through 9 only need to be done once. Step 10 onwards need to be done for each new experiment.

1) Setup an AMT requester account on https://requester.mturk.com/

When created, line your AMT requester account to an AWS account. (AMT is a service under the AWS umbrella, but you can in theory use it without 
making an AWS account. To use the developer mode, we need an aws account)

2) On https://requester.mturk.com/, go 'Developer' 

Here you should see a number of 'Steps'. Follow step 1, 2 and 3 on the requster.mturk webpage. Step 4 is not needed for our purposes.

3) STEP 1 Create an Amazon Web Services (AWS) Account
4) STEP 2 Link Your AWS Account with Your MTurk Requester Account (Be sure to copy your ACCESS KEY ID and SECRET ACCES KEY). If needed, the accounts can easily be unlinked later. 
5) STEP 3 Register for the MTurk Developer Sandbox. This is needed to properly test and develop our experiments without it costing real money. This sandbox account will be linked to your requester account.


Now that the required accounts have been set up with AMT, we can turn to the webserver. Access information will not be provided here (publicly visible) see the slack channel instead. If you do not have an account yet, ask Mitchell to set up a new account here. 

6) On the server, run the following command to enter the virtual enviroment

   	<code> source /home/labExperiment/labExperimentEnv/bin/activate </code>
	
7) Start the AWS configuration by running the following command. Be sure to substitute ADD_YOUR_NAMEf_HERE for your name, no spaces or special characters. This makes sure that when you run code on the server, it will be able to use your requester/sandbox account. 

   	<code> aws configure --profile ADD_YOUR_NAME_HERE </code>
	
8) Follow the propts and enter the ACCES KEY ID and SECRET ACCESS KEY. For Region name choose us-east-1, default output can be left blank
	Now, every time you run any code that makes connection with AMT it will use your AWS configuration on the server and thus your AWS account. 
	
9) Now run the following command to add your user profile to the database as well. 

	<code> ./manage.py make_new_experimenter --name ADD_YOUR_NAME_HERE </code>
	
10) The previosu steps created a configuration. We need to make sure that each time we use the server, the correct configuration is used. We do this by add this information in the bashrc file. 

	<code> nano ~/.bashrc  </code>
	
	go all the way to the bottom of the file and add the following
    
        AMT_BOTO_PROFILE="ADD_YOUR_NAME_HERE"; export AMT_BOTO_PROFILE
        alias lab='source /home/labExperiment/labExperimentEnv/bin/activate'
        alias labCelery='celery -A labExperiment worker -l INFO'

    save the file and reload your ssh window ( source ~/.bashrc). Now each time you log in to the server using your user account, it will automatically load in the configuration that was created in step 7/8. 

11) Make sure that Celery is running in an tmux window. Celery is a tasks queue, which keeps track and executes all asyncranous tasks. This functions as a load-balancer, i.e., if more people are submitting data to the server then can be handled, this will make sure it will not loose any data. TMUX enables permanent console windows on the server that don't close. However, they are unique per user. As such, we first log into the user created to run celery and then check if it is running. If it is not running, we start it. 

    	
	First, change into the celery user account. As your useraccount should have root access, we don't need the celeryuser password. 
	
    
    <code> sudo su celeryuser </code>
	
	Then, see all open tmux windows
        
   	<code> tmux ls </code>
   
   	If this returns 'celery: ....' then that means there's already a tmux window open so we can attach to that tmux window
                
   	<code> tmux attach -t celery</code>
   
   	If no tmux celery window was open before, we make a new one (and this automatically attached ourself to this window)
                        
   	<code> tmux new -s celery</code>
   
   	If celery is running, everything is set. Otherwise, first make sure we are connected to the labExperiment virtual enviroment (step 6) and then run celery:
	In the celery window, make sure we are connected to the labExperiment virtual enviromnet (step 6)
                        
   	<code> ./manage.py celery</code>
   
   	You can now exit tmux by 
                        
      <code>ctrl+b d</code>
      
      and return to your own user account with
      
     <code> exit </code>
   

12) To create a new experiment. First make sure you're in the virtual enviroment (step 6)
                                
      <code> cd /home/labExperiment</code>
                                
      <code> ./manage.py create_new_experiment --experiment YOUR_EXP_NAME_HERE</code>

13) For this experiment, make a new instance of that experiment.
                                        
      <code> cd /home/labExperiment</code>
                                        
      <code> ./manage.py create_new_experiment_instance --experiment YOUR_EXP_NAME_HERE --experiment_instance YOUR_EXP_INSTANCE_NAME_HERE </code>
	
      If you want to change settings for this version, change them in config.json. If you want to change them after running the experiment, better to create a new experiment instance

14) This will have created a a .html, .js and a .css file within the 'files' folder.
	Change the files to reflect your experiment. 
    In JS, Images can be accessed using the document.image_root variable. The condition can be accessed using the documnet.condition variable
	After making changes execute the "./manage.py reload" command from the /home/webExperiment folder so the server will be updated

15) You can test your experiment (not through AMT) by going to 

	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/0/
	
    Note that the last part of the url (/0/) indicates the condition. If you have multiple conditions, you can see the next conditions like so...
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/1/
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/2/ ..etc

    
16) Once everything is working as intended launch your experiment to SANDBOX
    make sure "MTURK_SANDBOX" in /home/webExperiment/settings.py is "True"

17) submit to AMT sandbox: 
                                            
      <code>./manage.py execute_experiment --experiment EXPERIMENT_NAME --experiment_instance EXPERIMENT_INSTANCE_NAME </code>
	


18) test everything, submit data. Are your functions and html working properly?

19) If yes, change  MTURK_SANDBOX to False in labExperiment.settings. This means that now the tasks will actually be submitted to mturk and not the sandbox

20) Repeat step 10, make sure that celery is running. Each change in code (except in .html, .css and, .js) will reload celery. If at any moment code is not valid, celery will fail. As such, make sure it is running. 

21) Run the ./manage execute again as in step 17
