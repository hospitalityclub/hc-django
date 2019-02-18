from cities_light.models import Country, Region, City
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields
from model_utils import Choices
import uuid
from .managers import AbstractObjectOwnerManager

# HC4 uses UUID for primary key of objects. It enables more thread-safe database operations and more API 
# options for manipulation of related model's new entities.
class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True, editable=False)
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, editable=False)

    # this allows to trace object ownership
    objects = AbstractObjectOwnerManager()

    class Meta:
        abstract = True


class Member(TranslatableModel, UUIDModel):

    # User model relationship, from which we inherit username, email, first_name, last_name, password, 
    # last_login and permission/group relationships.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='member',
        null=True,
        blank=True,
    )

    GENDER_CHOICES = Choices(
        ('male', _("male")),
        ('female', _("female")),
        ('transgender', _("transgender")),
        ('unspecified', _("unspecified")),
    )

    # TODO: make address a separate model with the ability to define primary one. Waiting for the decision of
    # Django Cities Light dependency acceptance
    # home_phone = models.TextField(_("Home Phone"), null=True, blank=True)
    # fax = models.TextField(_("Fax"), null=True, blank=True)

    photo = models.ImageField(_("photo"), blank=True, null=True, upload_to='member_photos')
    birthday = models.DateField(_("birth date"), blank=True, null=True)
    gender = models.CharField(_("gender"), max_length=8, choices=GENDER_CHOICES, default=GENDER_CHOICES.unspecified)
    email_2 = models.EmailField(_("email 2"), max_length=255, null=True, blank=True)
    mobile_phone = models.CharField(_("mobile phone"), max_length=32, null=True, blank=True)
    mobile_phone_2 = models.CharField(_("mobile phone 2"), max_length=32, null=True, blank=True)
    work_phone = models.TextField(_("work phone"), max_length=32, null=True, blank=True)
    home_page = models.URLField(_("home page"), max_length=255, null=True, blank=True)
    hide_name = models.BooleanField(_("hide my name"), default=False)
    offer_tour = models.BooleanField(_("offer to show around"), default=False)
    offer_dinner = models.BooleanField(_("offer dinner"), default=False)

    # only accepted members can host/visit/write other members
    accepted = models.BooleanField(_("accepted into Hospitality Club"), default=False)
    
    # Extra information
    translations = TranslatedFields(
        about_myself = models.TextField(_("about yourself"), max_length=4096, null=True, blank=True),
        occupation = models.CharField(_("occupation"), max_length=255, null=True, blank=True),
        organizations = models.TextField(_("member of organizations"), max_length=4096, null=True, blank=True,
                                        help_text=_("describe your activity in public organizations")),
    )

    # TODO:
    # feedback	varchar(255)	YES			
    # terms	tinyint(1)	YES			
    # category	int(11) unsigned	YES			
    # status	enum('buggy','false','problems','signed','true','needmore','morecompleted','kicked','takenout','sleeper','inactive','passedaway')	YES			
    # flags	varchar(255)	YES			
    # level	tinyint(4)	NO		0	
    # hcnotes	text	NO			
    # lastlogin	datetime	NO	MUL	0000-00-00 00:00:00	
    # ip	varchar(15)	NO			
    # vol_teaser	varchar(255)	YES			
    # vol_contact_info	varchar(255)	YES			
    # vol_why	varchar(255)	YES			
    # vol_what	varchar(255)	YES			
    # vol_additional	varchar(255)	YES			
    # emailerror	varchar(255)	YES			
    # lastaccess	datetime	YES			
    # chat_msn	varchar(255)	YES	MUL		
    # chat_icq	varchar(255)	YES			
    # chat_yahoo	varchar(255)	YES			
    # chat_skype	varchar(255)	YES	MUL		
    # chat_others	varchar(255)	YES			
    # chat_aol	varchar(255)	YES			
    # nbhost	int(2)	NO		0	
    # nbguest	int(2)	NO		0	
    # nbcomment	int(2)	NO		0	
    # visincity	tinyint(1)	YES		1	
    # visinlocation	tinyint(1)	YES	MUL	1	
    # nbtrust	int(2)	NO		0	
    # idcity	int(4)	NO	MUL	0	
    # nbpspcheck	int(2)	NO		0	
    # lang_signup	varchar(255)	YES			
    # lang_last	varchar(255)	YES			
    # nbvisit	int(8)	NO		0	
    # nbvisittoday	int(8)	NO		0	
    # myvisitidlist	varchar(255)	YES			
    # nbofremindreceivedsincelastlog	int(11)	NO		0	
    # nbofemailreceivedsincelastlog	int(11)	NO		0	
    # toberemind	datetime	YES			
    # attractions_updated	datetime	NO		0000-00-00 00:00:00	

    def __str__(self):
        if self.hide_name:
            return str(self.user.username)
        else:
            return '{} {} ({})'.format(self.user.first_name, self.user.last_name, self.user.username)

    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")


class Address(TranslatableModel, UUIDModel):
    ADDRESS_STATUS_CHOICES = Choices(
        ('closed', _("can not")),
        ('maybe', _("maybe")),
        ('open', _("open")),
    )

    postal_code = models.CharField(_("postal code"), max_length=16),
    latitude = models.DecimalField(_("latitude"), max_digits=8, decimal_places=6),
    longitude = models.DecimalField(_("longitude"), max_digits=8, decimal_places=6),
    
    city = models.ForeignKey(
        City,
        on_delete = models.PROTECT,
        related_name = 'addresses',
        verbose_name = _("city"),
    )
    
    member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'addresses',
        verbose_name = _("member"),
    )

    phone = models.CharField(_("phone"), max_length=32, null=True, blank=True)
    fax = models.CharField(_("fax"), max_length=32, null=True, blank=True)
    status = models.CharField(_("status"), max_length=16, choices=ADDRESS_STATUS_CHOICES, default=ADDRESS_STATUS_CHOICES.open)
    hide_location = models.BooleanField(_("hide my location"), default=False)

    # withgbfriend	tinyint(1)	YES		0	
    # withgrandpa	tinyint(1)	YES		0	
    # withpar	tinyint(1)	YES		0	
    # withsibs	tinyint(1)	YES		0	
    # withop	tinyint(1)	YES		0	
    # withalone	tinyint(1)	YES		0	
    # garden	tinyint(1)	YES		0	
    # spacefloor	tinyint(1)	YES		0	
    # matress	tinyint(1)	YES		0	
    # sofa	tinyint(1)	YES		0	
    # bed	tinyint(1)	YES		0	
    # ownroom	tinyint(1)	YES		0	
    # sleepother	longtext	YES			
    # bringtent	tinyint(1)	YES		0	
    # bringmat	tinyint(1)	YES		0	
    # bringsleep	tinyint(1)	YES		0	
    # numberguest	int(2) unsigned	YES	MUL		
    # staylength	int(2) unsigned	YES	MUL	0	
    # notifyshould	int(2) unsigned	YES	MUL	0	
    # notifymust	int(2) unsigned	YES	MUL	0	
    # callarrival	tinyint(1)	YES		0	
    # callbetween1	int(4)	YES		0	
    # callbetween2	int(4)	YES		0	
    # guestgender	enum('male','female','not_specified')	YES			
    # smoking	enum('allowed','disallowed','outside')	YES			
    # nodrugs	tinyint(1)	YES		0	
    # noalc	tinyint(1)	YES		0	
    # payphone	tinyint(1)	YES		0	
    # payfood	tinyint(1)	YES		0	
    # dodishes	tinyint(1)	YES		0	
    # restriother	varchar(255)	YES			
    # pets	varchar(255)	YES	MUL		
    # othcom	varchar(255)	YES	MUL		

    translations = TranslatedFields(
        street = models.CharField(_("street address"), max_length=255),
        best_times = models.CharField(_("best times to visit"), max_length=255),
        public_transport = models.TextField(_("public transport"), max_length=4096, null=True, blank=True),
        nearby_attractions = models.TextField(_("nearby attractions"), max_length=4096, null=True, blank=True),
        directions = models.TextField(_("directions"), max_length=4096, null=True, blank=True, 
                                      help_text=_("describe how to find your place")),
        offer_other = models.TextField(_("offer other"), max_length=4096, null=True, blank=True,
                                       help_text=_("describe what other services or activities you can offer to your guests")),
    )

    def get_region(self):
        return self.city.region

    def get_country(self):
        return self.city.country

    # TODO: Implement Nearby Big Cities
    def get_big_cities(self):
        pass

    def __str__(self):
        return '{}, {} {}, {}, {}'.format(self.street, self.postal_code, self.city, self.get_region(), self.get_country())

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")


class Language(UUIDModel):
    # We should consume this source - https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

    language = models.CharField(_("ISO language name"), max_length=32)
    language_native = models.CharField(_("native name"), max_length=32)
    iso639_1 = models.CharField(_("ISO 639-1 code"), max_length=2)
    iso639_2t = models.CharField(_("ISO 639-2/T code"), max_length=3)
    iso639_2b = models.CharField(_("ISO 639-2/B code"), max_length=3)

    def __str__(self):
        return self.language

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")


class MemberLanguage(UUIDModel):
    LANGUAGE_LEVELS = Choices(
        ('mother_tongue', _("mother tongue")),
        ('proficient', _("proficient")),
        ('advanced', _("advanced")),
        ('intermediate', _("intermediate")),
        ('beginner', _("beginner"))
    )

    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE, 
        related_name='member_languages', 
        verbose_name=_("member")
    )
    language = models.ForeignKey(
        Language, 
        on_delete=models.PROTECT, 
        related_name='member_languages', 
        verbose_name=_("language")
    )
    primary = models.BooleanField(_("primary"), default=False)
    level = models.CharField(_("level"), max_length=16, choices=LANGUAGE_LEVELS, default=LANGUAGE_LEVELS.mother_tongue)

    def __str__(self):
        return '{} ({})'.format(self.language, self.level)

    class Meta:
        verbose_name = _("member language")
        verbose_name_plural = _("member languages")


class Hobby(UUIDModel):
    hobby = models.CharField(_("hobby"), max_length=32)

    def __str__(self):
        return self.hobby

    class Meta:
        verbose_name = _("hobby")
        verbose_name_plural = _("hobbies")


class MemberHobby(UUIDModel):
    member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'member_hobbies',
        verbose_name = _("member")
    )

    hobby = models.ForeignKey(
        Hobby,
        on_delete = models.PROTECT,
        related_name = 'member_hobbies',
        verbose_name = _("hobby")
    )

    order = models.PositiveIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.hobby

    class Meta:
        verbose_name = _("member hobby")
        verbose_name_plural = _("member hobbies")


class MemberTravel(TranslatableModel, UUIDModel):
    member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'member_travels',
        verbose_name = _("member")
    )

    city = models.ForeignKey(
        City,
        on_delete = models.PROTECT,
        related_name = 'member_travels',
        verbose_name = _("city"),
    )

    hc_experience = models.BooleanField(_("HC experience"), default=True)
    visit_date_from = models.DateField(_("from"), auto_now_add=True)
    visit_date_to = models.DateField(_("to"), auto_now_add=True)
    plan = models.BooleanField(_("plan"), default=False)

    translations = TranslatedFields(
        feedback = models.TextField(_("feedback"), max_length=4096, null=True, blank=True),
    )

    def get_region(self):
        return self.city.region

    def get_country(self):
        return self.city.country

    def __str__(self):
        return '{}, {}, {}'.format(self.city, self.get_region(), self.get_country())

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

