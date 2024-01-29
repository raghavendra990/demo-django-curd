from django.db import models
import uuid

from userauth.log import LOGGER, raise_400 
from userauth.models import ModifiersBase, UserModel
# Create your models here.

ADD_ITEM_ISSUE = "Issue is adding data."
class Item(ModifiersBase, models.Model):

    id = models.UUIDField(primary_key = True, default=uuid.uuid1, blank=False, null=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_item')
    name = models.CharField(max_length = 50, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)


    class Meta:
        """
        Item meta info
        """
        ordering = ['created_at']

    @classmethod
    def add(cls, user, name, price):
        try:
            user_obj = UserModel(id=user)
            _obj = cls(user= user_obj, name= name, price=price, created_by=user, updated_by=user)
            _obj.save()
        except Exception as e:
             LOGGER.error(f'Error while processing Item add, {name=}, {e}')
             raise_400(ADD_ITEM_ISSUE)
        return _obj