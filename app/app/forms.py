from flask_wtf import Form
from wtforms import StringField, RadioField, BooleanField
from wtforms.validators import DataRequired, URL


class MapInput(Form):
    phrase1 = StringField()
    phrase2 = StringField()

    positioning1 = RadioField(
        label = "Position of phrase in name",
        choices = ["Starts", "Contains", "Ends"]
    )
    positioning2 = RadioField(
        label = "Position of phrase in name",
        choices = ["Starts", "Contains", "Ends"]
    )

    color1 = RadioField(
        label = "Color",
        choices=["Red", "Green", "Blue", "Purple", "Black"]
    )
    color2 = RadioField(
        label = "Color",
        choices=["Red", "Green", "Blue", "Purple", "Black"]
    )

    all_names = BooleanField()
    
    only_indepedent = BooleanField()
    only_official = BooleanField()
