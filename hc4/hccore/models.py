from cities_light.models import City, Country
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

    GENDER_CHOICES = Choices(
        ('male', _("male")),
        ('female', _("female")),
        ('transgender', _("transgender")),
        ('unspecified', _("unspecified")),
    )

    # status	enum('buggy','false','problems','signed','true','needmore','morecompleted','kicked','takenout','sleeper','inactive','passedaway')	YES			
    STATUS_CHOICES = Choices(
        ('active', _("active")),
        ('kicked', _("kicked and banned")),
        ('passedaway', _("passed away")),
        ('takenout', _("taken out")),
        ('sleeper', _("sleeper")),
        ('inactive', _("inactive")),
        ('true', _("true")),
        ('false', _("false")),
        ('problems', _("problems")),
        ('buggy', _("buggy")),
        ('signed', _("signed")),
        ('needmore', _("need more")),
        ('morecompleted', _("more completed")),
    )

    # User model relationship, from which we inherit username, email, first_name, last_name, password, 
    # last_login and permission/group relationships.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='member',
        null=True,
        blank=True,
    )

    photo = models.ImageField(_("photo"), blank=True, null=True, upload_to='member_photos')
    birthday = models.DateField(_("birth date"), blank=True, null=True)
    gender = models.CharField(_("gender"), max_length=8, choices=GENDER_CHOICES, default=GENDER_CHOICES.unspecified)

    # Contact Methods moved to separate model group
    # email_2 = models.EmailField(_("email 2"), max_length=255, null=True, blank=True)
    # mobile_phone = models.CharField(_("mobile phone"), max_length=31, null=True, blank=True)
    # mobile_phone_2 = models.CharField(_("mobile phone 2"), max_length=31, null=True, blank=True)
    # work_phone = models.TextField(_("work phone"), max_length=31, null=True, blank=True)
    # home_page = models.URLField(_("home page"), max_length=255, null=True, blank=True)
    hide_name = models.BooleanField(_("hide my name"), default=False)
    offer_tour = models.BooleanField(_("offer to show around"), default=False)
    offer_dinner = models.BooleanField(_("offer dinner"), default=False)

    # only accepted members can host/visit/write other members
    accepted = models.BooleanField(_("accepted into Hospitality Club"), default=False)
    # all members have to agree with HC terms and conditions, this is a valid signature
    agreed_with_terms = models.BooleanField(_("agreed with Hospitality Club Terms and Conditions"), default=True)
    status = models.CharField(_("status"), max_length=15, choices=STATUS_CHOICES, default=STATUS_CHOICES.active)
    ui_language = models.CharField(_("UI language"), max_length=7, default="en")
    
    # Extra information
    translations = TranslatedFields(
        about_myself = models.TextField(_("about yourself"), max_length=4095, null=True, blank=True),
        occupation = models.CharField(_("occupation"), max_length=255, null=True, blank=True),
        organizations = models.TextField(_("member of organizations"), max_length=4095, null=True, blank=True,
                                        help_text=_("describe your activity in public organizations")),
        internal_notes = models.TextField(_("internal notes"), null=True, blank=True,
                                          help_text=_("for HC volunteer eyes only")),
        feedback = models.TextField(_("feedback to HC"), max_length=4095, null=True, blank=True),
    )

    # TODO:
    # vol_teaser	varchar(255)	YES			
    # vol_contact_info	varchar(255)	YES			
    # vol_why	varchar(255)	YES			
    # vol_what	varchar(255)	YES			
    # vol_additional	varchar(255)	YES			
    # visincity	tinyint(1)	YES		1	
    # visinlocation	tinyint(1)	YES	MUL	1	
    # nbhost	int(2)	NO		0	
    # nbguest	int(2)	NO		0	
    # nbcomment	int(2)	NO		0	
    # nbtrust	int(2)	NO		0	
    # nbpspcheck	int(2)	NO		0	
    # nbvisit	int(8)	NO		0	
    # nbvisittoday	int(8)	NO		0	

    def __str__(self):
        if self.hide_name:
            return str(self.user.username)
        else:
            return '{} {} ({})'.format(self.user.first_name, self.user.last_name, self.user.username)

    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")


class Address(TranslatableModel, UUIDModel):
    # Address status will be binary for now
    # ADDRESS_STATUS_CHOICES = Choices(
    #     ('closed', _("can not host")),
    #     ('maybe', _("maybe can host")),
    #     ('open', _("open for guests")),
    # )

    PETS_CHOICES = Choices(
        ('no', _("no")),
        ('dog', _("dog(s)")),
        ('cat', _("cat(s)")),
        ('catsndogs', _("cats and dogs")),
        ('other', _("other")),
    )

    SMOKING_POLICY_CHOICES = Choices(
        ('no', _("not allowed at all, inside or outside")),
        ('yes', _("allowed inside")),
        ('balcony', _("allowed in the balcony, terrace or garden")),
        ('outside', _("allowed only outside")),
    )

    postal_code = models.CharField(_("postal code"), max_length=15, null=True, blank=True),
    latitude = models.DecimalField(_("latitude"), max_digits=8, decimal_places=6, default=0, db_index=True),
    longitude = models.DecimalField(_("longitude"), max_digits=8, decimal_places=6, default=0, db_index=True),
    
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

    phone = models.CharField(_("phone"), max_length=31, null=True, blank=True)
    fax = models.CharField(_("fax"), max_length=31, null=True, blank=True)
    status = models.BooleanField(_("accepting guests"), default=1) 
        #CharField(_("status"), max_length=15, choices=ADDRESS_STATUS_CHOICES, default=ADDRESS_STATUS_CHOICES.open)
    hide_location = models.BooleanField(_("hide my location"), default=False)

    # living with fields
    living_with_partner = models.BooleanField(_("living with partner"), default=0,
                                              help_text=_("boyfriend, girlfriend, wife, husband, etc."))
    living_with_parents = models.BooleanField(_("living with parents"), default=0)
    living_with_grandparents = models.BooleanField(_("living with grandparents"), default=0)
    living_with_siblings = models.BooleanField(_("living with siblings"), default=0)
    living_with_pets = models.CharField(_("living with pets"), max_length=31, choices=PETS_CHOICES, default=PETS_CHOICES.no)
    living_alone = models.BooleanField(_("living alone"), default=0)

    # hosting options
    own_room = models.PositiveSmallIntegerField(_("own room"), default=0, help_text=_("do you offer a private room?"))
    bed = models.PositiveSmallIntegerField(_("Bed"), default=0, help_text=_("do you offer to sleep in a bed?"))
    sofa = models.PositiveSmallIntegerField(_("sofa"), default=0, help_text=_("do you offer to sleep on a sofa?"))
    mattress = models.PositiveSmallIntegerField(_("mattress"), default=0, help_text=_("do you offer a mattress (on the floor)?"))
    space_on_the_floor = models.BooleanField(_("space on the floor"), default=0, help_text=_("do you offer only space on the floor?"))
    garden = models.BooleanField(_("garden"), default=0, help_text=_("do you have a garden?"))
    sleep_together = models.BooleanField(_("sleep together"), default=0, 
        help_text=_("will your guests have to sleep with you or other people? People in guests travel company does not count."))
    bring_sleeping_bag = models.BooleanField(_("guest must bring own sleeping bag"), default=0)
    bring_mattress = models.BooleanField(_("guest must bring own mattress"), default=0)
    bring_tent = models.BooleanField(_("guest must bring own tent"), default=0)
    max_guests = models.PositiveSmallIntegerField(_("maximum guests allowed"), default=1, db_index=True, 
        help_text=_("how many guests maximum can you host at once?"))

    # limitations to the guests
    max_stay_length = models.PositiveSmallIntegerField(_("maximum stay length"), default=0, db_index=True)
    should_notify = models.PositiveSmallIntegerField(_("how many days ahead guest should confirm the arrival?"), default=0)
    must_notify = models.PositiveSmallIntegerField(_("how many days ahead guest must confirm the arrival?"), default=0)
    call_on_arrival = models.BooleanField(_("does guest have to phone call on arrival?"), default=0)
    do_not_call_before = models.TimeField(_("do not call before"), default=0)
    do_not_call_after = models.TimeField(_("do not call after"), default=0)
    guest_gender = models.CharField(_("preferred guest gender"), max_length=8, choices=Member.GENDER_CHOICES, 
                                    default=Member.GENDER_CHOICES.unspecified)
    smoking = models.CharField(_("smoking policy"), max_length=8, choices=SMOKING_POLICY_CHOICES, default=SMOKING_POLICY_CHOICES.no)
    no_drugs = models.BooleanField(_("drugs are not allowed"), default=1)
    no_alcohol = models.BooleanField(_("alcohol is not allowed"), default=1)
    pay_for_food = models.BooleanField(_("pay for consumed food"), default=0)
    pay_for_comm = models.BooleanField(_("pay for used communication"), default=0, 
                                       help_text=_("guests have the ability to use and to pay for phone minutes, metered internet traffic"))
    do_dishes = models.BooleanField(_("do dishes"), default=0)
    pets_allowed = models.CharField(_("pets allowed"), max_length=31, choices=PETS_CHOICES, default=PETS_CHOICES.no, db_index=True)

    # translatable fields have to be dumped into this container
    translations = TranslatedFields(
        street = models.CharField(_("street address"), max_length=255),
        best_times = models.CharField(_("best times to visit"), max_length=255),
        public_transport = models.TextField(_("public transport"), max_length=4095, null=True, blank=True),
        nearby_attractions = models.TextField(_("nearby attractions"), max_length=4095, null=True, blank=True),
        directions = models.TextField(_("directions"), max_length=4095, null=True, blank=True, 
                                      help_text=_("describe how to find your place")),
        offer_other = models.TextField(_("offer other"), max_length=4095, null=True, blank=True,
                                       help_text=_("describe what other services or activities you can offer to your guests")),
        living_with_other_persons = models.CharField(_("living with other persons"), max_length=255, null=True, blank=True),
        other_restrictions = models.TextField(_("other restrictions"), max_length=4095, null=True, blank=True),
        additional_info = models.TextField(_("additional information"), max_length=4095, null=True, blank=True),
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


class ContactMethod(TranslatableModel, UUIDModel):
    icon_class = models.CharField(_("icon class"), max_length=31, null=True, blank=True, help_text=_("CSS icon class"))
    icon_image = models.ImageField(_("icon image"), upload_to='img/icons', null=True, blank=True)
    url_prefix = models.URLField(_("URL prefix"), max_length=63, help_text=_("for example, for Telegram: http://t.me/"))

    translations = TranslatedFields(
        name = models.CharField(_("name"), max_length=31, help_text=_("examples: mobile phone, Telegram, alternate email"))
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("contact method")
        verbose_name_plural = _("contact methods")


class MemberContact(UUIDModel):
    member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'member_contacts',
        verbose_name = _("member"),
    )

    contact_method = models.ForeignKey(
        ContactMethod,
        on_delete = models.PROTECT,
        related_name = 'member_contacts',
        verbose_name = _("contact method")
    )

    contact_detail = models.CharField(_("contact detail"), max_length=255, blank=True)
    preferred = models.BooleanField(_("preferred"), default=0)
    share_by_default = models.BooleanField(_("share by default"), default=1)

    def __str__(self):
        return '{}: {}'.format(self.contact_method, self.contact_detail)

    class Meta:
        verbose_name = _("member contact")
        verbose_name_plural = _("member contacts")


class Language(UUIDModel):
    # We should consume this source - https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

    language = models.CharField(_("ISO language name"), max_length=31)
    language_native = models.CharField(_("native name"), max_length=31)
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
    level = models.CharField(_("level"), max_length=15, choices=LANGUAGE_LEVELS, default=LANGUAGE_LEVELS.mother_tongue)

    def __str__(self):
        return '{} ({})'.format(self.language, self.level)

    class Meta:
        verbose_name = _("member language")
        verbose_name_plural = _("member languages")


class Hobby(UUIDModel):
    hobby = models.CharField(_("hobby"), max_length=31)

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
        feedback = models.TextField(_("feedback"), max_length=4095, null=True, blank=True),
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


class MemberLoginHistory(UUIDModel):
    member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'member_login_history',
        verbose_name = _("member"),
    )
    ip_address = models.IPAddressField(_("IP Address")),
    ip_country = models.ForeignKey(
        Country,
        on_delete = models.PROTECT,
        related_name = 'member_login_history',
        verbose_name = _("country of IP address")
    )
    ip_latitude = models.DecimalField(_("latitude"), max_digits=8, decimal_places=6, default=0),
    ip_longitude = models.DecimalField(_("longitude"), max_digits=8, decimal_places=6, default=0),
    latitude = models.DecimalField(_("latitude"), max_digits=8, decimal_places=6, default=0),
    longitude = models.DecimalField(_("longitude"), max_digits=8, decimal_places=6, default=0),

    def __str__(self):
        return '{} / {} / {}'.format(self.ip_address, self.ip_country, self.created_at)

    class Meta:
        verbose_name = _("member login history")
        verbose_name_plural = _("member login history")


class MemberRelation(UUIDModel):
    from_member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'member_relations_sender',
        verbose_name = _("from member"),
    )

    to_member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'member_relations_recipient',
        verbose_name = _("to member"),
    )

    follow = models.BooleanField(_("follow"), default=False)
    trust = models.BooleanField(_("trust"), default=False)
    was_guest = models.BooleanField(_("was guest"), default=False)
    was_host = models.BooleanField(_("was host"), default=False)

    # identity cross check
    identify = models.BooleanField(_("identify"), default=False, help_text=_("I have checked member's passport or ID"))
    was_identified = models.BooleanField(_("was identified"), default=False, help_text=_("my passport or ID was chedked by member"))

    comment = models.TextField(_("comment"), max_length=4095)
    reported_inappropriate = models.BooleanField(_("reported inappropriate"), default=False)
    confirmed_inappropriate = models.BooleanField(_("confirmed inappropriate"), default=False)

    def __str__(self):
        return '{} - {}'.format(self.from_member, self.to_member)

    class Meta:
        verbose_name = _("member relation")
        verbose_name_plural = _("member relations")

class Message(UUIDModel):
    from_member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'message_sender',
        verbose_name = _("from member"),
    )

    to_member = models.ForeignKey(
        Member,
        on_delete = models.CASCADE,
        related_name = 'message_recipient',
        verbose_name = _("to member"),
    )

    message = models.TextField(_("message"), max_length=4095, blank=True, null=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    is_spam = models.BooleanField(_("is spam"), default=False)

    def __str__(self):
        return '{} - {}'.format(self.from_member, self.to_member)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("message")
