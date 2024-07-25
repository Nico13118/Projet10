from django.db import models, transaction


class Project(models.Model):
    objects = models.Manager()
    TYPE = [
        ('BA', 'back-end'),
        ('FE', 'front-end'),
        ('IOS', 'iOS'),
        ('AND', 'Android')
    ]
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='project_author')
    contributors = models.ManyToManyField('User', through='Contributor', related_name='project_contributor')
    project_name = models.CharField(max_length=200, blank=False)
    project_description = models.TextField(max_length=8192, blank=False)
    type = models.CharField(max_length=3, choices=TYPE, blank=False)

    def __str__(self):
        return self.project_name


class Contributor(models.Model):
    objects = models.Manager()
    date_joined = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='contributor_user')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='contributor_project')

    def __str__(self):
        return f"{self.user} - {self.project}"


class Issue(models.Model):
    objects = models.Manager()
    PRIORITY = [
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH')
    ]
    TAG = [
        ('BUG', 'BUG'),
        ('FEATURE', 'FEATURE'),
        ('TASK', 'TASK')
    ]
    STATUS = [
        ('TO DO', 'TO DO'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('FINISHED', 'FINISHED')
    ]
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author_issue')
    assigned_contributor = models.ForeignKey('User', on_delete=models.CASCADE, blank=False)
    issue_name = models.CharField(max_length=200, blank=False)
    issue_description = models.TextField(max_length=8192, blank=False)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_issue')
    priority = models.CharField(max_length=6, choices=PRIORITY, blank=False)
    tag = models.CharField(max_length=7, choices=TAG, blank=False)
    status = models.CharField(max_length=11, choices=STATUS, default='TO DO')

    def __str__(self):
        return f"{self.author} - {self.assigned_contributor} - {self.issue_name}"
