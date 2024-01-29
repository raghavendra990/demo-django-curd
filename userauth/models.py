from django.db import models, transaction
import uuid
from django.utils import timezone
import hashlib

from .log import LOGGER, raise_400 
# Create your models here.

REGISTER_ISSUE = 'Issue registering user.'
class CreatedMixin(models.Model):
    """ CreatedMixin """
    created_at = models.DateTimeField( auto_now_add=True)
    created_by = models.UUIDField(null=True)

    class Meta:
        """ ModifiersBase Meta """
        abstract = True


class ModifiersBase(CreatedMixin, models.Model):
    """
    Base class with standard modifier fields
    created_at, updated_at, created_by, updated_by
    """
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.UUIDField(null=True)

    class Meta:
        """ ModifiersBase Meta """
        abstract = True

class UserModel(ModifiersBase , models.Model):


    id = models.UUIDField(primary_key = True, default=uuid.uuid1, blank=False, null=False)
    username = models.CharField(db_index=True, max_length = 50)
    password = models.CharField(max_length=100, null=True)

    def hash_password( password, salt):
        password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return password_hash

    def verify_password( stored_password, provided_password, salt):
        password_hash = hashlib.sha256((provided_password + salt).encode('utf-8')).hexdigest()
        return password_hash == stored_password
        
    @classmethod
    def register(cls, username, password):
        try:
            hashed_password = cls.hash_password(password, username)
            _obj = cls(username= username, password= hashed_password)
            _obj.save()
        except Exception as e:
             LOGGER.error(f'Error while processing Register data, {username=}, {e}')
             raise_400(REGISTER_ISSUE)
        return _obj

class BlackListedToken(models.Model):
    token = models.CharField(max_length=500, db_index=True)
    user = models.ForeignKey(UserModel, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")