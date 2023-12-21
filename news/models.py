from django.db import models
from django.utils import timezone
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class NewsItemTag(models.Model):
    
    TAG_CHOICES = [
        ('ACL', 'Ashesi Champions League'),
        ('APL', 'Ashesi Premier League'),
        ('AFA Cup', 'Ashesi Football Association Cup'),
        ('Course Clash Cup', 'Course Clash Cup'),
        ('Inter-Class Cup', 'Inter-Class Cup'),
        ('Transfer', 'Transfer'),
        ('Injury', 'Injury'),
        ('Match Preview', 'Match Preview'),
        ('Match Report', 'Match Report'),
        ('Interview', 'Interview'),
        ('Opinion', 'Opinion'),
        ('Feature', 'Feature'),
        ('Tactical Analysis', 'Tactical Analysis'),
        ('Presser', 'Press Conference'),
        ('Other', 'Other')
    ]
    
    name = models.CharField(max_length=200, null=False, blank=False, choices=TAG_CHOICES, unique=True)

    def __str__(self):
        return self.name
    
# Define default tags
DEFAULT_TAGS = [
    'ACL',
    'APL',
    'AFA Cup',
    'Transfer',
    'Injury',
    'Match Preview',
    'Match Report',
    'Interview',
    'Opinion',
    'Feature',
    'Tactical Analysis',
    'Presser',
    'Other',
]

# Signal handler to create default tags after migration
@receiver(post_migrate)
def create_default_tags(sender, **kwargs):
    if sender.name == 'news':
        for tag in DEFAULT_TAGS:
            NewsItemTag.objects.get_or_create(name=tag)
            

class NewsItem(models.Model):
    featured_image = models.CharField(max_length=200, null=False, blank=False, default=None)
    title = models.TextField(null=False, blank=False)
    subtitle = models.CharField(max_length=200, null=False, blank=False)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    text = models.TextField()
    author = models.ForeignKey('account.Fan', on_delete=models.SET_DEFAULT, related_name='news_items', null=True, blank=True, default=None)
    tag = models.ForeignKey(NewsItemTag, on_delete=models.SET_DEFAULT, related_name='news_items', null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    @property
    def was_published_today(self):
        return self.pub_date.date() == timezone.now().date()

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'news items'
