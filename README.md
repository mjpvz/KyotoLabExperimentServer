If you wish to run experiments on Amazon Mechnical Turk, you will first need to follow steps 1 through 10. You will only need this once. 
If you instead wish to run experiments on Prolific or just locally, you can skip ahead to step 11. 
If you have already completed the set up and used the server before, you can continue straight ahead to step 12. 

# Setting up for Amazon Mechnical Turk

1) Setup an AMT requester account on https://requester.mturk.com/

	When created, link your AMT requester account to an AWS account. (AMT is a service under the AWS umbrella, but you can in theory use it without 
	making an AWS account. To use the developer mode, we need an aws account)

2) On https://requester.mturk.com/, go 'Developer' 

	Here you should see a number of 'Steps'. Follow step 1, 2 and 3 on the requster.mturk webpage. Step 4 is not needed for our purposes.

3) STEP 1 Create an Amazon Web Services (AWS) Account
4) STEP 2 Link Your AWS Account with Your MTurk Requester Account (Be sure to copy your <code>ACCESS KEY ID</code> and <code>SECRET ACCES KEY</code>). If needed, the accounts can easily be unlinked later. 
5) STEP 3 Register for the MTurk Developer Sandbox. This is needed to properly test and develop our experiments without it costing real money. This sandbox account will be linked to your requester account.


	Now that the required accounts have been set up with AMT, we can turn to the webserver. Access information will not be provided here (publicly visible) see the slack channel instead. If you do not have an account yet, ask Mitchell to set up a new account here. 

6) On the server, run the following command to enter the virtual enviroment

   	<code> source /home/labExperiment/labExperimentEnv/bin/activate </code>
	
7) Start the AWS configuration by running the following command. Be sure to substitute <code>ADD_YOUR_NAMEf_HERE</code> for your name. The name is a string variable that can be anything as long as it identifies you and used no spaces or special characters. Together with the next few steps, this will make sure that when you run code on the server, it will be able to use your requester/sandbox account. 

   	<code> aws configure --profile ADD_YOUR_NAME_HERE </code>
	
8) Follow the prompts and enter the <code>ACCES KEY ID</code> and <code>SECRET ACCESS KEY</code>. For Region name choose <code>us-east-1</code>, default output can be left blank
	Now, every time you run any code that makes connection with AMT it will use your AWS configuration on the server and thus your AWS account. 
	
9) Now run the following command to add your user profile to the database as well. Note that the <code>ADD_YOUR_NAME_HERE</code> NEEDS be identical to the one used in step 7/8

	<code> ./manage.py make_new_experimenter --name ADD_YOUR_NAME_HERE </code>
	
10) The previous steps created an AMT configuration. We need to make sure that each time we use the server, the correct configuration is used. We do this by add this information in the bashrc file. On Ubuntu, a bashrc file is automatically created for each user and each time that user connects to the server, this file will be loaded. As such, any settings declared in this file will be loaded only for this user. 

	<code> nano ~/.bashrc  </code>
	
	go all the way to the bottom of the file and add the following line
    
        AMT_BOTO_PROFILE="ADD_YOUR_NAME_HERE"; export AMT_BOTO_PROFILE

    save the file and reload your ssh window with <code> source ~/.bashrc </code>. Now each time you log in to the server using your user account, it will automatically load in the configuration that was created in step 7/8. 
    
# First time creating experiments.

11) First we will add some shortcuts to our Ubuntu user profile via the bashrc file. On Ubuntu, a bashrc file is automatically created for each user and each time that user connects to the server, this file will be loaded. As such, any settings or shortcuts declared in this file will be loaded for this user. 

	<code> nano ~/.bashrc  </code>
	
	go all the way to the bottom of the file and add the two following lines
    
        alias lab='source /home/labExperiment/labExperimentEnv/bin/activate'
        alias labCelery='celery -A labExperiment worker -l INFO'

    save the file and reload your ssh window with <code> source ~/.bashrc </code>. Now each time you log in to the server using your user account, it will automatically load in these shortcuts. We only need to do this once. 
    
# Running an experiment. 

12) Run the following command to enter the virtual enviroment. This will add a <code> (labExperimentEnv) </code> in front of your username on the server if it worked. 

   	<code> source /home/labExperiment/labExperimentEnv/bin/activate </code>
	
	You should also be able to use <code> lab </code> instead, as it is a shortcut we created in step 11. 

13) Make sure that Celery is running in an TMUX window. **Celery** is a tasks queue, which keeps track and executes all tasks running in the background. This functions as a load-balancer, i.e., if many people are submitting data to the server at the same time, the server might not be able to handle it. Celery will make sure the tasks are handled one at a time and will make sure it will not loose any data and/or fail any tasks. **TMUX** enables permanent console windows on the server that don't close. That is, if you start any program in your current console, and close the console the program will be terminated. TMUX is one way to keep programs running, even when closing the terminal. However, they are unique per user. As such, we must first log into the user that was created specifically to run celery and then check if it is running. If it is not running, we start it. 

    	
	First, change into the celery user account with the following command. As your useraccount should have root access, we don't need the celeryuser password. 
	
    <code> sudo su celeryuser </code>
	
	Then, we shall see if there are any open TMUX windows with the following command. Unless something went wrong with the server, there should indeed already be a TMUX window. 
        
   	<code> tmux ls </code>
   
   	If this returns 'celery: ....' then that means there's already a TMUX window open so we can attach to that tmux window
                
   	<code> tmux attach -t celery</code>
   
   	If instead no TMUX celery window was open before, we make a new one automatically attached ourself to this new window. 
                        
   	<code> tmux new -s celery</code>
   
   	If celery is running, everything is already set up and we can continue to step 13. You can see if celery is running if the input starts all the way at the left, and if you can not see <code> (labExperiment) your_username </code> on the input line. Otherwise, we will start Celery. First make sure we are connected to the labExperiment virtual enviroment (step 12) and then run celery:
                        
   	<code> /home/labExperiment/manage.py celery</code>
   
   	You can now exit tmux by using
                        
      <code>ctrl+b d</code>
      
      Now we are still logged in as the Celery useraccount. So return to your own user account with, this should change 
      
     <code> exit </code>
   

14) To create a new experiment project,  perform this step. If you already have an experimental project, skip to the next step.  First make sure you're in the virtual enviroment (step 12) and then execute the following.
                                
      <code> cd /home/labExperiment</code>
      
      Then execute the following command and carefully read the text in the console. It will further guide you to create this experiment. 
                                
      <code> ./manage.py create_new_experiment </code>
      
      Now a new experiment project has been created. On the server an 'experiment project' is the overarching concept that connects multiple experiments. For example, 
      if we want to run a number of visual search experiments, each with slightly different stimuli or parameters, then all these experiments would belong to a single experiment project. This allows us to keep similar experiments collected within the same project, and keeps everything structured and clean.


15) For this experiment project, make a new instance of that experiment. In one experiment project we can have multiple different instances. First make sure you're in the virtual enviroment (step 12) and then execute the following.
                                
      <code> cd /home/labExperiment</code>
                                                                               
      <code> ./manage.py create_new_experiment_instance </code>
      
      The command will ask some questions. Read them carefully. Once this is completed, the command will have created a <code>.html</code>, <code>.js</code> and a <code>.css</code> file within the 'files' folder.
	
	
16) Whenever we make any changes to the .js files, we need to tell the server those files have been updated. Creating the files, like in the previous step also counts as a change. Thus, now and **each time you make changes to the .js files**, we run the following commands. If we do not run this step, the server will keep using the old .js files. In some cases this might look like there is no problem, but it can cause to big errors! 

	First, go to the correct directory
	<code> cd /home/labExperiment</code> and then run:
	
	<code> ./reload.sh </code> 
	
	
17) You can now 'see' your experiment by navigating the browser to the following URL, be sure to change the URL with your names

	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_PROJECT_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/0/
	
    Note that the last part of the url (, i..e, /0/) indicates the condition. If you have multiple conditions, you can see the next conditions like so...
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/1/
	https://labexperiment.cog.ist.i.kyoto-u.ac.jp/experiments/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE/2/ ..etc
	If you don't want to use conditions, you can just stay using the /0/ version without any issue. 
	
	
18) Now update the code within the .html, .css and .js files to reflect your desired experiment. In the .js file, the current condition can be accessed using the document.condition variable. For images, place them within the <code> stimuli </code> folder. The path to the images can accessed with the document.image_root folder. 

    The images themselves will be hosted at
    
    https://labexperiment.cog.ist.i.kyoto-u.ac.jp/static/experiments/current/YOUR_EXP_NAME_HERE/stimuli/STIMULI_FILE_NAME.jpg" 

19) Once the experiment is finished, call the <code> submit_data </code> function, and pass the data you wish to save on the server along as a dictionary. Test if this works a few times. If everything appears to work, you can move on to the next section. 

# Run the experiment and gather data

20) Repeat step 13 and make sure that celery is running. Each change in code (except in <code>.html</code>, <code>.css</code> and, <code>.js</code>) will reload celery. If at any moment code is not valid (which is very likely), celery will fail and not start until we do it manually. As such, make sure it is running. 

21) If you want to use prolific go to the prolific secetion.  If you AMT, continue with steps . 
    
    
# Run the experiment and gather data with PROLIFIC - this currently does not work! Check back later. 

22) On prolific, click on <code> New Study </code> and fill out <code> Study Details </code> as desired. 


24) At the <code> STUDY LINK </code> section, first enter the URL to your experiment (see step 18). For each condition, create a separate study. 


26) After entering the URL, click the <code>  I'll use URL parameters  </code> button. This will add some important parameters to the URL. Without these parameters the experiment will not be able to be completed.  

27) At the <code> STUDY COMPLETION </code> section, click the <code>  I'll redirect them using an URL  </code> option. 

28) Copy the URL that prolific generated, which should look something like this <code> https://app.prolific.co/submissions/complete?cc=COMPLETION_CODE </code> and place it into the .html file for your experiment (experiments/current/YOUR_EXP_NAME_HERE/YOUR_EXP_INSTANCE_NAME_HERE.html. In the HTML you will see a variable:

      window.PROLIFIC_SUBMISSION_URL = 'REPLACE_WITH_THE_URL_PROLIFIC_GAVE_YOU_IF_RUNNING_ON_PROLIFIC'
      
      Replace this value with the URL we just copied. 
      
29) Continue with the AUDIENCE and STUDY COST sections. You can test everything with the PREVIEW button. If everything works (be sure to check if data is succesfully submitted to the server!) you can PUBLISH the experiment! 
  
    
# Run the experiment and gather data on AMT - this currently does not work after some changes were made! No rush to update this for now. 
  
23) Once everything is working as intended launch your experiment to SANDBOX
    Change the <code>MTURK_SANDBOX</code> variable in /home/webExperiment/settings.py to "True"

24) submit to AMT sandbox. This means it will go the AMT platform, but it won't cost any money yet. As such, we can do some final checks. 
      
      <code>./manage.py execute_experiment --experiment EXPERIMENT_NAME --experiment_instance EXPERIMENT_INSTANCE_NAME </code>
	

25) Go to the mechnical turk sandbox and look for the experiment we just submitted there. Test everything, submit data, etc. Are your functions and html working properly?

26) If everything appears to work, change <code>MTURK_SANDBOX</code> to False in labExperiment.settings. This means that now the tasks will actually be submitted to mturk and not the sandbox. This will require money to be associated with your AMT account. 

27) Run the ./manage execute again as in step 18. This time it will send experiments to AMT and participants will be able to see and do your tasks. 
