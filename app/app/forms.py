from flask_wtf import Form
from wtforms import StringField, RadioField, BooleanField
from wtforms.validators import DataRequired, URL


class MapInput(Form):
    phrase1 = StringField(validators=[DataRequired()])
    phrase2 = StringField(validators=[DataRequired()])

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
        choices=["Red", "Green", "Blue", "Purple", "Black"],
        default = "Red"
    )
    color2 = RadioField(
        label = "Color",
        choices=["Red", "Green", "Blue", "Purple", "Black"],
        default = "Blue"
    )

    all_names = BooleanField( label="Use all names" )
    
    only_indepedent = BooleanField(label="Use only names without superior name" )
    only_official = BooleanField(label="Use only official names")
