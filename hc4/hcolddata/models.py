# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cities(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    region_id = models.IntegerField(blank=True, null=True)
    other_names = models.CharField(max_length=255, blank=True, null=True)
    near_city_names = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    isvalidflag = models.IntegerField()
    geofinfo = models.TextField()
    nbmembersformap = models.IntegerField()
    selectable = models.IntegerField(blank=True, null=True)
    nbmembers = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cities'


class Comments(models.Model):
    from_member = models.IntegerField()
    to_member = models.IntegerField()
    comment = models.TextField()
    created = models.DateTimeField()
    type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'comments'


class Countries(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    regionopen = models.IntegerField()
    members = models.IntegerField(blank=True, null=True)
    hcworld_created = models.DateTimeField(blank=True, null=True)
    idnation = models.IntegerField(blank=True, null=True)
    idcapital = models.IntegerField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    continent = models.IntegerField(blank=True, null=True)
    flag = models.CharField(max_length=2, blank=True, null=True)
    spamindex = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class Members(models.Model):
    country_id = models.PositiveIntegerField()
    city_id = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=13, blank=True, null=True)
    username = models.CharField(max_length=255)
    accepted = models.IntegerField(blank=True, null=True)
    city_volunteer = models.IntegerField(blank=True, null=True)
    region_volunteer = models.IntegerField(blank=True, null=True)
    country_volunteer = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    homephone = models.CharField(max_length=255, blank=True, null=True)
    workphone = models.CharField(max_length=255, blank=True, null=True)
    mobilephone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    updates = models.IntegerField()
    secstreet = models.CharField(max_length=255, blank=True, null=True)
    seccity = models.CharField(max_length=255, blank=True, null=True)
    secregion = models.CharField(max_length=255, blank=True, null=True)
    seczip = models.CharField(max_length=255, blank=True, null=True)
    seccountry = models.PositiveIntegerField()
    secphone = models.CharField(max_length=255, blank=True, null=True)
    secinfo = models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    hobbies = models.CharField(max_length=255, blank=True, null=True)
    organizations = models.CharField(max_length=255, blank=True, null=True)
    travels = models.TextField(blank=True, null=True)
    plans = models.TextField(blank=True, null=True)
    aboutmyself = models.TextField(blank=True, null=True)
    accom = models.PositiveIntegerField(blank=True, null=True)
    offershow = models.IntegerField(blank=True, null=True)
    offerdinner = models.IntegerField(blank=True, null=True)
    offerother = models.CharField(max_length=255, blank=True, null=True)
    besttimes = models.CharField(max_length=255, blank=True, null=True)
    publictrans = models.CharField(max_length=255, blank=True, null=True)
    bigcities = models.CharField(max_length=255, blank=True, null=True)
    attractions = models.CharField(max_length=255, blank=True, null=True)
    withgbfriend = models.IntegerField(blank=True, null=True)
    withgrandpa = models.IntegerField(blank=True, null=True)
    withpar = models.IntegerField(blank=True, null=True)
    withsibs = models.IntegerField(blank=True, null=True)
    withop = models.IntegerField(blank=True, null=True)
    withalone = models.IntegerField(blank=True, null=True)
    garden = models.IntegerField(blank=True, null=True)
    spacefloor = models.IntegerField(blank=True, null=True)
    matress = models.IntegerField(blank=True, null=True)
    sofa = models.IntegerField(blank=True, null=True)
    bed = models.IntegerField(blank=True, null=True)
    ownroom = models.IntegerField(blank=True, null=True)
    sleepother = models.TextField(blank=True, null=True)
    bringtent = models.IntegerField(blank=True, null=True)
    bringmat = models.IntegerField(blank=True, null=True)
    bringsleep = models.IntegerField(blank=True, null=True)
    numberguest = models.PositiveIntegerField(blank=True, null=True)
    staylength = models.PositiveIntegerField(blank=True, null=True)
    notifyshould = models.PositiveIntegerField(blank=True, null=True)
    notifymust = models.PositiveIntegerField(blank=True, null=True)
    callarrival = models.IntegerField(blank=True, null=True)
    callbetween1 = models.IntegerField(blank=True, null=True)
    callbetween2 = models.IntegerField(blank=True, null=True)
    guestgender = models.CharField(max_length=13, blank=True, null=True)
    smoking = models.CharField(max_length=10, blank=True, null=True)
    nodrugs = models.IntegerField(blank=True, null=True)
    noalc = models.IntegerField(blank=True, null=True)
    payphone = models.IntegerField(blank=True, null=True)
    payfood = models.IntegerField(blank=True, null=True)
    dodishes = models.IntegerField(blank=True, null=True)
    restriother = models.CharField(max_length=255, blank=True, null=True)
    pets = models.CharField(max_length=255, blank=True, null=True)
    othcom = models.CharField(max_length=255, blank=True, null=True)
    feedback = models.CharField(max_length=255, blank=True, null=True)
    terms = models.IntegerField(blank=True, null=True)
    category = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=13, blank=True, null=True)
    flags = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField()
    hcnotes = models.TextField()
    name = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    secemail = models.CharField(max_length=255)
    namehide = models.IntegerField(blank=True, null=True)
    streethide = models.IntegerField(blank=True, null=True)
    lastlogin = models.DateTimeField()
    ip = models.CharField(max_length=15)
    vol_teaser = models.CharField(max_length=255, blank=True, null=True)
    vol_contact_info = models.CharField(max_length=255, blank=True, null=True)
    vol_why = models.CharField(max_length=255, blank=True, null=True)
    vol_what = models.CharField(max_length=255, blank=True, null=True)
    vol_additional = models.CharField(max_length=255, blank=True, null=True)
    emailerror = models.CharField(max_length=255, blank=True, null=True)
    lastaccess = models.DateTimeField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    chat_msn = models.CharField(max_length=255, blank=True, null=True)
    chat_icq = models.CharField(max_length=255, blank=True, null=True)
    chat_yahoo = models.CharField(max_length=255, blank=True, null=True)
    chat_skype = models.CharField(max_length=255, blank=True, null=True)
    chat_others = models.CharField(max_length=255, blank=True, null=True)
    chat_aol = models.CharField(max_length=255, blank=True, null=True)
    nbhost = models.IntegerField()
    nbguest = models.IntegerField()
    nbcomment = models.IntegerField()
    visincity = models.IntegerField(blank=True, null=True)
    visinlocation = models.IntegerField(blank=True, null=True)
    nbtrust = models.IntegerField()
    idcity = models.IntegerField()
    nbpspcheck = models.IntegerField()
    lang_signup = models.CharField(max_length=255, blank=True, null=True)
    lang_last = models.CharField(max_length=255, blank=True, null=True)
    nbvisit = models.IntegerField()
    nbvisittoday = models.IntegerField()
    myvisitidlist = models.CharField(max_length=255, blank=True, null=True)
    nbofremindreceivedsincelastlog = models.IntegerField()
    nbofemailreceivedsincelastlog = models.IntegerField()
    toberemind = models.DateTimeField(blank=True, null=True)
    attractions_updated = models.DateTimeField()
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'members'


class Messages(models.Model):
    from_member = models.IntegerField()
    to_member = models.IntegerField()
    message = models.TextField()
    created = models.DateTimeField()
    type = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'messages'


class Regions(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    other_names = models.TextField(blank=True, null=True)
    isvalidate = models.IntegerField()
    country_id = models.IntegerField()
    citiesopen = models.IntegerField()
    selectable = models.IntegerField(blank=True, null=True)
    hcworld_created = models.DateTimeField(blank=True, null=True)
    main_city_id = models.IntegerField(blank=True, null=True)
    nbmembers = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'regions'


class Relations(models.Model):
    from_member = models.IntegerField(blank=True, null=True)
    to_member = models.IntegerField(blank=True, null=True)
    following = models.IntegerField(blank=True, null=True)
    trust = models.IntegerField(blank=True, null=True)
    guest = models.IntegerField(blank=True, null=True)
    host = models.IntegerField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relations'
