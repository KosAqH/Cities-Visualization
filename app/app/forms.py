from flask_wtf import Form
from wtforms import StringField, RadioField, BooleanField
from wtforms.validators import DataRequired, URL


class MapInput(Form):
    phrase = StringField()

    positioning = RadioField(
        label = "Position of phrase in name",
        choices = ["Starts", "Contains", "Ends"]
    )

    color = RadioField(
        label = "Color",
        choices=["Red", "Green", "Blue", "Purple", "Black"]
    )

    all_names = BooleanField()
    
    only_indepedent = BooleanField()
    only_official = BooleanField()
