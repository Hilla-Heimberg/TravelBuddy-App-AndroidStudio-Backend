import os
from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

class SectionContent(Model):
    """
    A representation of an image and its processing status.
    When the processing is completed, the ProcessedImage model should contain the S3 bucket and key
    for the processed image.
    """
    class Meta:
        region = os.environ["AWS_DEFAULT_REGION"]
        table_name = "travel-buddy-sections-content"

    user_id = UnicodeAttribute(hash_key=True)
    Flights = UnicodeAttribute(null=True)
    Accommodation = UnicodeAttribute(null=True)
    Car_rental = UnicodeAttribute(null=True)
    Expenses = UnicodeAttribute(null=True)
    Food_and_Drinks = UnicodeAttribute(null=True)
    Equipment_list = UnicodeAttribute(null=True)
    Travel_destinations = UnicodeAttribute(null=True)
    Shopping = UnicodeAttribute(null=True)
    Transportation = UnicodeAttribute(null=True)
    Weather = UnicodeAttribute(null=True)
    Important_information = UnicodeAttribute(null=True)
    Addition = UnicodeAttribute(null=True)
