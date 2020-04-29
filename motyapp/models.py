# api/models.py

from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return '%s %s' % (self.title, self.body)

class BotResponse(models.Model):
    bot_response_id = models.AutoField(primary_key=True)
    search_str = models.TextField()
    response_str = models.TextField()
    
    def to_json(self):
        return {"bot_response_id":self.bot_response_id, "search_str":self.search_str, "response_str" : self.response_str}

    class Meta:
        managed = True
        db_table = 'bot_response'
