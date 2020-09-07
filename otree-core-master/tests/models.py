import easymoney
from otree.common import currency_range
from otree.db import models
import otree.models
import otree.forms
from otree import widgets


class Subsession(otree.models.BaseSubsession):
    pass


class SimpleModel(otree.models.BaseGroup):
    name = models.CharField()

    def name_choices(self):
        return [(self.name, self.name.upper())]


class SimplePlayer(otree.db.models.Model):
    name = otree.db.models.CharField(max_length=50, blank=True)
    age = otree.db.models.IntegerField(default=30, null=True, blank=True)


class FormFieldModel(otree.models.BaseGroup):
    null_boolean = models.BooleanField()
    big_integer = models.BigIntegerField()
    boolean = models.BooleanField(default=False)
    char = models.CharField()
    comma_separated_integer = models.CommaSeparatedIntegerField(max_length=100)
    date = models.DateField()
    date_time = models.DateTimeField()
    alt_date_time = models.DateTimeField(
        widget=otree.forms.SplitDateTimeWidget
    )
    decimal = models.DecimalField(max_digits=5, decimal_places=2)
    email = models.EmailField()
    file = models.FileField(upload_to='_tmp/uploads')
    file_path = models.FilePathField()
    float = models.FloatField()
    integer = models.IntegerField()
    generic_ip_address = models.GenericIPAddressField()
    positive_integer = models.PositiveIntegerField()
    positive_small_integer = models.PositiveSmallIntegerField()
    slug = models.SlugField()
    small_integer = models.SmallIntegerField()
    text = models.TextField()
    alt_text = models.TextField(widget=otree.forms.TextInput)
    time = models.TimeField()
    url = models.URLField()
    many_to_many = models.ManyToManyField('SimpleModel', related_name='+')
    one_to_one = models.OneToOneField('SimpleModel', related_name='+')

    currency = models.CurrencyField()
    currency_choice = models.CurrencyField(
        choices=[('0.01', '0.01'), ('1.20', '1.20')])

    sent_amount = models.CurrencyField(choices=currency_range(0, 0.75, 0.05))
    slider_widget = models.IntegerField(widget=widgets.SliderInput())


class CurrencyFieldTestModel(otree.db.models.Model):
    currency_with_default_value_zero = models.CurrencyField(
        initial=easymoney.Money(0), min=0)
