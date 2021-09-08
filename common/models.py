from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# TODO make sure these exists/work/are needed
from mturk.utils import get_mturk_connection, is_mturk_sandbox, \ 
    get_or_create_mturk_worker, extract_mturk_attr, \
    qualification_dict_to_boto, ExternalQuestion



# Create your models here.

class EmptyModelBase(models.Model):
    """ Base class of all models, with no fields """

    added = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)

class UserProfile(EmptyModelBase):
    """ Additional data on top of Django User model """

    #: Django user instance (contains username, hashed password, etc).  This
    #: also forms the primary key, so ``User`` and ``UserProfile`` instances have
    #: the same primary key.
    user = models.OneToOneField(
        User, unique=True, primary_key=True, related_name="profile",on_delete=models.PROTECT)

    #: Mechanical Turk Worker ID
    mturk_worker_id = models.CharField(max_length=127, blank=True)

    #: block user (only locally; not on mturk) 
    # Workers can be blocked both in general, for all tasks, or per task through ExperimentWorker
    blocked = models.BooleanField(default=False)

    #: reason for blocking -- this will be displayed to the user to the user when the user tries to load a task
    blocked_reason = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.__unicode__()

    def block(self, reason='', save=True):
        """ Block a user from performing *all* MTurk tasks.  Note that Amazon
        is not contacted and the worker's account is not flagged. """

        self.blocked = True
        self.blocked_reason = reason
        if save:
            self.save()
        print('Blocking user: {} , reason: {}'.format(self.user.username, self.blocked_reason))


    def unblock(self, save=True):
        """ Unblock a user (undo the ``self.block()`` operation). """

        self.blocked = False
        self.blocked_reason = ''
        if save:
            self.save()

    def contact(self, subject, message):
        """ Send an email message to this AMT user through the AMT platform. """
        from mturk.utils import get_mturk_connection

        if len(subject) >= 200:
            raise Exception('The maximum subject size is 200 characters')
        if len(message) >= 4096:
            raise Exception('The maximum message size in 4096 characters')

        client = get_mturk_connection()
        client.notify_workers(
            Subject=subject,
            MessageText=message,
            WorkerIds=[self.mturk_worker_id] # the API function exists to contact multiple workers, so wrap id in array
        )

class ExperimentInstance(EmptyModelBase):
    """ Settings for creating new HITs (existing HITs do not use this data).  """

    #: reward per HIT
    reward = models.DecimalField(decimal_places=4, max_digits=8)

    #: external question info
    external_url = models.CharField(max_length=255)

    #: number of output instances expected
    num_outputs_max = models.IntegerField(default=5)

    #: number of content_type objects per hit
    contents_per_hit = models.IntegerField(default=1)

    #: vertical size of the frame in pixels
    frame_height = models.IntegerField(default=800)

    #: metadata shown to workers when listing tasks on the marketplace
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=1000)  # comma-separated list

    #: time (seconds) the worker has to complete the task
    duration = models.IntegerField(default=60 * 60)

    #: time (seconds) that the task is on the market
    lifetime = models.IntegerField(default=3600 * 24 * 5)

    #: time (seconds) until the task is automatically approved
    auto_approval_delay = models.IntegerField(default=60 * 60 * 24 * 2)

    #: json-encoded dictionary: amazon-enforced limits on worker history (e.g.
    #: assignment accept rate)
    qualifications = models.TextField(default='{}')

    #: bonus for giving feedback
    bonus_amount = models.DecimalField(
        decimal_places=2, max_digits=8, null=True, blank=True)

    def get_external_question(self):
        return ExternalQuestion(
            external_url=self.external_url,
            frame_height=self.frame_height)


     def get_hit_type(**kwargs):
    """ Returns a HIT type and also manages attaching the requirements list. If no hit type exists yet with this configuration, a new one will be made """

        # unpack from json if string
        if isinstance(self.requirements, basestring):
            reqs = json.loads(reqs)
        if isinstance(self.qualifications, basestring):
            quals = json.loads(quals)

        # disable qualifications on the sandbox. 
        if settings.MTURK_SANDBOX:
            qual_req = []
        else:
            qual_req = qualification_dict_to_boto(quals)
            # count number of quals, max is ten. If more then 10, raise an error

        # parse rward into a string, with max 2 decimals
        reward = self.experiment_instance.reward
        reward = str(round(float(reward),2))

        # send request to Amazon
        response = get_mturk_connection().create_hit_type( # This will return the existing hit_type if it already exists
            Title=self.title,
            Description=self.description,
            Reward=reward,
            AssignmentDurationInSeconds=self.duration,
            Keywords=self.keywords,
            AutoApprovalDelayInSeconds=self.auto_approval_delay,
            QualificationRequirements=qual_req)

        hit_type_id = extract_mturk_attr(response, 'HITTypeId')
        return hit_type_id


class Experiment(EmptyModelBase):
    """ High-level separation of HITs.  """

    # settings used for generating new HITs
    new_hit_settings = models.ForeignKey(
        ExperimentInstance, related_name="experiments", null=True, blank=True,on_delete=models.PROTECT)

    #: slug: url and filename-safe name of this experiment. is also the name used for templates.
    slug = models.CharField(max_length=32, db_index=True)

    #: A descriptive name of the experiment 
    name = models.CharField(max_length=128)

    # A description of the e

    #: whether there is a dedicated tutorial for this task
    has_tutorial = models.BooleanField(default=False) 

    #: directory where the template is stored.  the templates for each
    #: experiment are constructed as follows:
    #:
    #:     {template_dir}/{slug}.html              -- mturk task
    #:     {template_dir}/{slug}_inst.html         -- instructions 
    #:     {template_dir}/{slug}_tut.html          -- tutorial (if there is one)
    template_dir = models.CharField(
        max_length=255, default='mturk/experiments')

    def save(self, *args, **kwargs):
        super(Experiment, self).save(*args, **kwargs)

    def external_task_url(self):
	    return settings.SITE_URL + reverse('mturk-external-task',args=(self.id,)) 

    def template_name(self):
        return os.path.join(self.template_dir, self.slug)



   

class ExperimentWorker(EmptyModelBase):
    """ The stats for a worker and a given experiment.  """

    #: Experiment being done
    experiment = models.ForeignKey(Experiment, related_name='experiment_workers')

    #: Worker performing the experiment
    worker = models.ForeignKey(UserProfile, related_name='experiment_workers', on_delete=models.PROTECT)

    #: If the experiment has a tutorial, this records whether the tutorial was
    #: completed.
    tutorial_completed = models.BooleanField(default=False)

    #: block user (only locally; not on mturk)
    blocked = models.BooleanField(default=False)

    #: reason for blocking -- message to be displayed to the user
    blocked_reason = models.TextField(blank=True)

    def contact(self, subject, message):
        """ A wrapper to call the UserProfile parent of this ExperimentWorker instance """
        self.worker.contact(subject, message)


    def block(self, reason='', all_tasks=False,
              report_to_mturk=False, save=True):
        """ Prevent a user from working on tasks in the future.  Unless
        ``report_to_mturk`` is set, This is only local to your server and the
        worker's account on mturk is not flagged.
        :param reason: A message to display to the user when they try and
            complete tasks in the future.
        :param all_tasks: if ``True``, block the worker from all experiments.
        :param report_to_mturk: if ``True``, block the worker from all experiments,
            and also block them from MTurk.  This will flag the user's account, so only
            use this for malicious users who are clearly abusing your task.
        """

        self.blocked = True
        self.blocked_reason = reason
        if save:
            self.save()
        if all_tasks or report_to_mturk:
            # Block on all tasks
            self.worker.block(reason=reason, save=True)


class MtHit(MtModelBase):
    """ MTurk HIT (Human Intelligence Task, corresponds to a MTurk HIT object) """

    #: use Amazon's id
    mturk_id = models.CharField(max_length=128, primary_key=True)
    hit_type = models.CharField(max_length=128, blank=True) # will be set by ExperimentInstance.get_hit_type

    lifetime = models.IntegerField(null=True, blank=True)
    expired = models.BooleanField(default=False)
    sandbox = models.BooleanField(default=(is_mturk_sandbox))

    #: if True, at least one assignment has been submitted (useful for filtering)
    any_submitted_assignments = models.BooleanField(default=False)
    #: if True, all assignments have been submitted (useful for filtering)
    all_submitted_assignments = models.BooleanField(default=False)

    # assignment data -- only updated after a sync
    max_assignments = models.IntegerField(default=1)
    num_assignments_available = models.IntegerField(null=True, blank=True)
    num_assignments_completed = models.IntegerField(null=True, blank=True)
    num_assignments_pending = models.IntegerField(null=True, blank=True)


    #: dictionary converting MTurk attr names to model attr names
    str_to_attr = {
        'LifetimeInSeconds': 'lifetime',
        'MaxAssignments': 'max_assignments',
        'NumberOfAssignmentsAvailable': 'num_assignments_available',
        'NumberOfAssignmentsCompleted': 'num_assignments_completed',
        'NumberOfAssignmentsPending': 'num_assignments_pending',
        'expired': 'expired'  # yes, this is lower case in boto (and documented)
    }

    HIT_STATUSES = (
        ('A', 'Assignable'),
        ('U', 'Unassignable'),
        ('R', 'Reviewable'),
        ('E', 'Reviewing'),
        ('D', 'Disposed'),
    )
    str_to_hit_status = dict((v, k) for (k, v) in HIT_STATUSES)
    hit_status_to_str = dict((k, v) for (k, v) in HIT_STATUSES)
    hit_status = models.CharField(
        max_length=1, choices=HIT_STATUSES, null=True, blank=True)



    def save(self, *args, **kwargs):
        if not self.mturk_id:
            self.sandbox = settings.MTURK_SANDBOX
            self.hit_status = 'A'

            # send request to Amazon
            response = get_mturk_connection().create_hit_with_hit_type(
                HITTypeId=self.hit_type.mturk_id,
                Question=self.hit_type.get_external_question().get_as_xml(),
                LifetimeInSeconds=self.lifetime,
                MaxAssignments=self.max_assignments,
                RequesterAnnotation=json.dumps(
                    {
                        u'experiment_id': self.hit_type.experiment.id,
                        u'num_contents': self.contents.count(),
                    })
            )
            self.id = extract_mturk_attr(response, 'HITId')
        elif self.hit_status != 'D':  # 'D': disposed     

            # add any missing attributes
            for k, v in MtHit.str_to_attr.iteritems():
                if getattr(self, v) is None:
                    aws_hit = self.get_aws_hit()
                    try:
                        k = extract_mturk_attr(aws_hit, k)
                        setattr(self, v, k)
                    except Exception: # raised when extract_mturk_attr can't find it
                        pass

        super(MtHit, self).save(*args, **kwargs)

    def sync_status(self, hit=None, sync_assignments=True):
        """ Set this instance status to match the Amazon status.  """

        connection = get_mturk_connection()
        if not hit:
            hit = self.get_aws_hit(connection)


        self.hit_status = MtHit.str_to_hit_status[hit['HIT']['HITStatus']]
        
        for k, v in MtHit.str_to_attr.iteritems():
            if hasattr(hit, k):
                setattr(self, v, hit['HIT'][k])

        if sync_assignments:
            assignment_ids = []

            num_submitted = 0
            page = 1
            token = False
            while True:
                if not token:
                    page_data = connection.list_assignments_for_hit(
                        HITId=self.id, MaxResults=100)
                else:
                     page_data = connection.list_assignments_for_hit(
                        HITId=self.id, MaxResults=100, NextToken = token)    

                for data in page_data['Assignments']:
                    ass_id = data['AssignmentId']
                    assignment_ids.append(ass_id)
                    assignment = self.assignments \
                        .get_or_create(id=ass_id)[0]
                    assignment.sync_status(data)
                    if assignment.status is not None:
                        num_submitted += 1
                # as long as there are more results, AMT sends a pagination token along
                try:
                    token = page_data['NextToken']
                except KeyError:
                    break

            # extra assignments should have None status
            self.assignments.exclude(id__in=assignment_ids) \
                .update(status=None)

            # NOTE: the int() is needed since self.max_assignments
            # is set above, and is still a unicode string at this point
            self.any_submitted_assignments = (num_submitted > 0)
            self.all_submitted_assignments = (
                num_submitted >= int(self.max_assignments))

        self.save()

    def get_aws_hit(self, connection=None):
        if not connection:
            connection = get_mturk_connection()
        return connection.get_hit(HITId=self.id)

    def expire(self, data=None, date=datetime.datetime(2015,1,1) ):
        """ Expire this HIT -- no new workers can accept this HIT, but existing
        workers can finish """

        if self.expired:
            self.sync_status(data)
            if self.expired:
                print("Already expired..")
                return False

        if not self.expired:
            print('Expiring: {}'.format(self.id)
            get_mturk_connection().update_expiration_for_hit(
                HITId=self.id,
                ExpireAt = date # a date in the past will be expired as soon as possible
             )
            self.expired = True
            self.save()

            return True
    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "HIT"
        verbose_name_plural = "HITs"



class MtAssignment(MtModelBase):
    """
    An assignment is a worker assigned to a HIT
    NOTE: Do not create this -- they should be automatically created when a participant opens a task.
    If something appears wrong, call sync_status() on a MtHit object
    """

    #: use the Amazon-provided ID as our ID
    mturk_id = models.CharField(max_length=128, primary_key=True)

    hit = models.ForeignKey(MtHit, related_name='assignments',on_delete=models.PROTECT)
    worker = models.ForeignKey(UserProfile, related_name='assignments', null=True, blank=True,on_delete=models.PROTECT)

    #: set by Amazon and updated using sync_status
    accept_time = models.DateTimeField(null=True, blank=True)
    #: set by Amazon and updated using sync_status
    submit_time = models.DateTimeField(null=True, blank=True)
    #: set by Amazon and updated using sync_status
    approval_time = models.DateTimeField(null=True, blank=True)
    #: set by Amazon and updated using sync_status
    rejection_time = models.DateTimeField(null=True, blank=True)
    #: set by Amazon and updated using sync_status
    deadline = models.DateTimeField(null=True, blank=True)
    #: set by Amazon and updated using sync_status
    auto_approval_time = models.DateTimeField(null=True, blank=True)

    str_to_attr = {
        'AcceptTime': 'accept_time',
        'AutoApprovalTime': 'auto_approval_time',
        'SubmitTime': 'submit_time',
        'Deadline': 'deadline',
        'ApprovalTime': 'approval_time',
        'RejectionTime': 'rejection_time',
    }

    #: bonus for good job 
    bonus = models.DecimalField(
        decimal_places=2, max_digits=8, null=True, blank=True)

    #: message(s) given to the user after different operations.
    #: if multiple messages are sent, they are separated by '\n'.
    bonus_message = models.TextField(blank=True)
    approve_message = models.TextField(blank=True)
    reject_message = models.TextField(blank=True)

    #: user-agent string from last submit.
    user_agent = models.TextField(blank=True)

    #: user screen size
    screen_width = models.IntegerField(null=True, blank=True)
    #: user screen size
    screen_height = models.IntegerField(null=True, blank=True)

    #: json-encoded request.POST dictionary from last submit.
    post_data = models.TextField(blank=True)

    #: json-encoded request.META dictionary from last submit.
    #: see: https://docs.djangoproject.com/en/dev/ref/request-response/
    post_meta = models.TextField(blank=True)

    #: estimate of the time spent doing the HIT
    time_ms = models.IntegerField(null=True, blank=True)

    #: estimate of the time spent doing the HIT, excluding time where the user
    #: is in another window
    time_active_ms = models.IntegerField(null=True, blank=True)

    #: estimate of how long the page took to load; note that this ignores server
    #: response time, so this will always be ~300ms smaller than reality.
    time_load_ms = models.IntegerField(null=True, blank=True)

    #: estimate of the wage from this HIT
    wage = models.FloatField(null=True, blank=True)

    #: If ``True``, then the async task (``mturk.tasks.mturk_submit_task``) has
    #: finished processing what the user submitted.  Note that there is a period
    #: of time (sometimes up to an hour depending on the celery queue length)
    #: where the assignment is submitted (``status == 'S'``) but the responses
    #: are not inserted into the database.
    submission_complete = models.BooleanField(default=False)

    ASSIGNMENT_STATUSES = (
        ('S', 'Submitted'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )
    str_to_status = dict((v, k) for (k, v) in ASSIGNMENT_STATUSES)
    status_to_str = dict((k, v) for (k, v) in ASSIGNMENT_STATUSES)
    status = models.CharField(
        max_length=1, choices=ASSIGNMENT_STATUSES,
        null=True, blank=True)

    def approve(self, feedback=None, save=True):
        """ Send command to Amazon approving this assignment """

        if self.status == 'A':
            self.hit.sync_status() # TODO check sync_status
            if self.status == 'A':
                return

        if self.status == 'R':
            print('Un-rejecting assignment: {}, experiment: {}, expired: {}'.format(
                self.id, self.hit.hit_type.experiment.slug, self.hit.expired)
            if not feedback:
                feedback = "We have un-rejected this assignment and approved it.  We are very sorry."
            self.reject_message = feedback
            get_mturk_connection().approve_assignment( # this can only been done upto 30 days after initial rejection
                AssignmentId=self.id, 
                RequesterFeedback=feedback,
                OverrideRejection = True)
        else:
            # check if its not already approved, because then this will give an error.

            if not feedback:
                feedback = "Thank you!"

            client = get_mturk_connection() 
            resp = client.get_assignment(AssignmentId=self.id)
            status = extract_mturk_attr(resp,'AssignmentStatus')
            if not status == u'Approved':
            print('Approving assignment: {}, experiment: {}, expired: {}'.format(
                    self.id, self.hit.hit_type.experiment.slug, self.hit.expired)
                self.approve_message = feedback
                client.approve_assignment(
                    AssignmentId=self.id,
                    RequesterFeedback=feedback)

        self.status = 'A'

        if save:
            self.save()

    def reject(self, feedback=None, save=True):
        """ Send command to Amazon rejecting this assignment. 
        In practise we should only reject assignmetns in extreme measures. Otherwise, approve and simply block the user.  

        :param feedback:
            message shown to the user
        :param save:
            whether to save the result in the database (should always be
            ``True``) unless you are already saving the model again shortly
            after.
        """
        if not feedback:
            feedback = "I'm sorry but you made too many mistakes."

        if self.status == 'A' or self.status == 'R':
            self.hit.sync_status()
            if self.status == 'A' or self.status == 'R':
                return

        print('Rejecting assignment: {}, experiment: {}, expired: {}'.format(
            self.id, self.hit.hit_type.experiment.slug, self.hit.expired)
        get_mturk_connection().reject_assignment(
            AssignmentId=self.id, RequesterFeedback=feedback)
        self.reject_message = feedback
        self.status = 'R'
        if save:
            self.save()


    def grant_bonus(self, price, reason, save=True):

        price = str(price)
        if eval(price) > 5:
            raise Exception("The bonus price ({}) is too high. Is this correct?".format(price))
    
        if self.status == 'S':
            self.approve(feedback=reason)

        print('Granting bonus: {}s, price: ${}, reason: {}').format(self.id, price, reason)
        connection = get_mturk_connection()
        connection.send_bonus(
            WorkerId=str(self.worker.mturk_worker_id),
            AssignmentId=self.id,
            BonusAmount=price,
            Reason=reason
        )

        if self.bonus:
            self.bonus += Decimal(price)
        else:
            self.bonus = Decimal(price)

        if self.bonus_message:
            self.bonus_message += '\n' + reason
        else:
            self.bonus_message = reason
            
        if save:
            self.save()


    def sync_status(self, data):
        """ data: instance of boto.mturk.connection.Assignment """
        self.worker = get_or_create_mturk_worker(data['WorkerId'])
        self.status = MtAssignment.str_to_status[data['AssignmentStatus']]
        for k, v in MtAssignment.str_to_attr.iteritems():
            if hasattr(data, k):
                setattr(self, v, data[k])
        self.save()

    def save(self, *args, **kwargs):
        if self.id == 'ASSIGNMENT_ID_NOT_AVAILABLE':
            # just in case anyone tries to save the preview assignment id, abort
            return

        # fix some fields that sometimes get messed up
        if self.time_ms < 0:
            self.time_ms = 0
        if self.time_active_ms < self.time_ms:
            self.time_active_ms = self.time_ms
        if self.submission_complete is None:
            self.submission_complete = False
	if self.has_feedback and self.feedback:
            self.feedback_length = len(self.feedback)
        else:
            self.feedback_length = 0

        if not self.wage and (self.time_ms or self.time_active_ms):
            time = self.time_active_ms if self.time_active_ms else self.time_ms
            self.wage = float(self.hit.hit_type.reward) * 3600000.0 / time

        super(MtAssignment, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
