import boto3
from decimal import Decimal
from common.models import UserProfile


def get_mturk_connection():
    """ Connect to the aws mturk client. Credentials are stored using awscli """
    from config import settings_local
    raise Exception('Still needs to be configured somehow...')
    return boto3.client(
        'mturk',
        aws_access_key_id = settings_local.MTURK_AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings_local.MTURK_AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.MTURK_HOST, 
        region_name='us-east-1')


def get_mturk_balance():
    response = get_mturk_connection().get_account_balance()
    return Decimal(extract_mturk_attr(response,'AvailableBalance'))


def get_or_create_mturk_worker(mturk_worker_id):
    """ Returns a UserProfile object for the associated mturk_worker_id """
    if not mturk_worker_id:
        return None
    try:
        return UserProfile.objects.get(mturk_worker_id=mturk_worker_id)
    except UserProfile.DoesNotExist:
        user, _ = User.objects.get_or_create(
            username='mturk_' + mturk_worker_id)
        profile = user.profile
        profile.mturk_worker_id = mturk_worker_id
        profile.save()
        return profile

def extract_mturk_attr(response, attr):
    """ Extracts an attribute from a boto ResultSet. """

    def get(target,dic):
        try:
            if target in dic.keys():
                return dic[target]
        except TypeError:
            pass
        except AttributeError:
            pass
        return False

    found = get(attr, response)
    if found:
        return found                                                                                                                         
    for key, value in response.items():
        if type(value) == dict: # nested 2  deep
            found = get(attr, value)
            if found:
                return found
            else:               # nested 3 deep, i don't think it goes deepepr. Otherwise we'll use a generator
                for key_, value_ in value.items():
                    found = get(attr,value_)
                    if found:
                        return found

    raise Exception('Missing {} in response'.format(attr)

def qualification_to_boto(name, value):
    """ Convert a qualification to the format required by boto """

    # comparators
    less = 'LessThanOrEqualTo'
    more = 'GreaterThanOrEqualTo'
    equal= 'EqualTo'

    
    # local_requirement is the only one which requires a different keyword in the qualifications call
    if name == 'local_requirement':
        id = '00000000000000000071'
        comparator = equal
        if value == "1" or value == 1:
            value = {"Country":'US'}
        else:
            raise Exception('Value needs to be an integer. 1 represents US. Add others you want here. Value = {}'.format(value))
    # some of these ID's are no longer in the official documentation, instead I tookt them
    # from the old boto source code. They work, but they might break any moment
    elif name == 'num_approved':
        id = '00000000000000000040'
        comparator=more
    elif name == 'perc_abandoned':
        id = '00000000000000000070'
        comparator=less
    elif name == 'perc_approved':
        id = '000000000000000000L0'
        comparator=more
    elif name == 'perc_rejected':
        id = '000000000000000000S0'
        comparator=less
    elif name == 'perc_returned':
        id = '000000000000000000E0'
        comparator=less
    elif name == 'perc_submitted':
        id = '00000000000000000000'
        comparator=more
    else:
        if not q and not name == 'local_requirement' : # if not a custom qualification, and name not known 
            raise ValueError("Unknown name: %s" % name)
    
    qual_rec_dic = {
        'QualificationTypeId':id,
        'Comparator': comparator,
        'RequiredToPreview':True,
        'ActionsGuarded' :'PreviewAndAccept'
    }

    if name == 'local_requirement':
        qual_rec_dic['LocaleValues'] = [value]
    else:
        qual_rec_dic['IntegerValues'] = [value]
    
    return qual_rec_dic