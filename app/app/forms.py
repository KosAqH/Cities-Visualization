from flask_wtf import Form
from wtforms import StringField, RadioField, BooleanField
from wtforms.validators import DataRequired, URL

class MapInput(Form):
    """
    Class defines MapInput form using flask_wtf
    """
    phrase1 = StringField(validators=[DataRequired()])
    phrase2 = StringField(validators=[DataRequired()])

    positioning1 = RadioField(
        label = "Position of phrase in name",
        choices = ["Starts", "Contains", "Ends"],
        validators=[DataRequired()],
        default = "Starts"
    )
    positioning2 = RadioField(
        label = "Position of phrase in name",
        choices = ["Starts", "Contains", "Ends"],
        validators=[DataRequired()],
        default = "Starts"
    )

    color1 = RadioField(
        label = "Color",
        choices=["Red", "Blue", "Green", "Purple", "Black"],
        default = "Red",
        validators=[DataRequired()]
    )
    color2 = RadioField(
        label = "Color",
        choices=["Red", "Blue", "Green", "Purple", "Black"],
        default = "Blue",
        validators=[DataRequired()]
    )
    
    only_indepedent = BooleanField(label="Use only names without superior name" )
    only_official = BooleanField(label="Use only official names")

    type_plot = RadioField(
        label = "Type of plot",
        choices=["Static", "Dynamic"],
        default = "Static",
        validators=[DataRequired()]
    )
