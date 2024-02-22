import uuid
from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """
    This is the base model that holds the common model fields
    across children models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Event(BaseModel):
    """
    This model is a representation of the event table
    in database.
    """
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    capacity = models.IntegerField(default=0)
    
    class Meta:
        db_table = "event"

class EventRegistration(BaseModel):
    """
    This model is a representation of the registration
    table in database.
    """
    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    booked_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "event_registration"

    def __str__(self):
        return f"{self.registration_id} : {self.booked_by.email}"

    def __unicode__(self):
        return self.registration_id

