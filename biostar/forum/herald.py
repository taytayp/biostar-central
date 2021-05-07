import logging
from django import forms
from django.template import loader
from django.conf import settings
from biostar.accounts.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from biostar.planet.models import Blog
from biostar.forum import auth, util
from biostar.forum.models import Post, SharedLink
from biostar.utils.decorators import is_moderator, authenticated

from .const import *


logger = logging.getLogger("engine")

MIN_CHARS = 5
MAX_CONTENT = 15000
MIN_CONTENT = 5
MAX_TITLE = 400
MAX_TAGS = 5

class HeraldSubmit(forms.Form):
    url = forms.CharField(min_length=10, max_length=MAX_CONTENT, required=True)
    text = forms.CharField(widget=forms.Textarea(attrs=dict(rows='5')), max_length=MAX_CONTENT, required=False,
                           strip=False)

    def __init__(self, user=None,  *args, **kwargs):
        self.user = user
        super(HeraldSubmit, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(HeraldSubmit, self).clean()
        url = cleaned_data['url']
        exists = SharedLink.objects.filter(url=url).first()

        if self.user.is_anonymous:
            raise forms.ValidationError("You need to be logged in.")

        if exists:
            raise forms.ValidationError("This link already exists.")

        # Low rep users can submit one link for consideration.
        if self.user.profile.low_rep:
            raise forms.ValidationError("Your reputation is too low .")

        return cleaned_data


def render_template(template, context):
    tmpl = loader.get_template(template_name=template)
    content = tmpl.render(context)
    return content


def herald_planet(post):
    """
    Create a herald blog post from a post.
    """

    blog = Blog.objects.filter()

    return


def herald_publisher(limit=20, nmin=1):
    """
    Create one publication from Herald accepted submissions ( up to 'limit' ).
    """

    # Slice heralds and
    # re-fetch query so we can apply .update() later
    heralds = SharedLink.objects.filter(status=SharedLink.ACCEPTED)[:limit]

    if heralds.count() < nmin:
        logger.warning(f"There aren't enough stories to publish, minimum of {nmin} required.")
        return

    # Create herald issue
    date = util.now()
    title = f"Biostar Herald {date.date()}"

    port = f':{settings.HTTP_PORT}' if settings.HTTP_PORT else ''
    base_url = f"{settings.PROTOCOL}://{settings.SITE_DOMAIN}{port}"

    context = dict(heralds=heralds, title=title, site_domain=settings.SITE_DOMAIN,
                   protocol=settings.PROTOCOL, base_url=base_url)
    content = render_template(template="herald/herald_content.md", context=context)

    # Create post user
    user = User.objects.filter(is_superuser=True).first()
    post = auth.create_post(title=title, content=content, author=user, tag_val='BiostarHerald', ptype=Post.HERALD)

    # Tie these submissions to a post
    hpks = heralds.values_list('pk', flat=True)
    SharedLink.objects.filter(pk__in=hpks).update(status=SharedLink.PUBLISHED, post=post, lastedit_date=date)

    # Log the action
    auth.db_logger(user=user, text=f"published {hpks.count()} submissions in {title}")

    # Create planet blog post linking to this herald issue.
    return post


@is_moderator
def herald_list(request):
    """
    List latest herald_list items
    """

    # List newly submitted links.
    stories = SharedLink.objects.order_by('-creation_date')
    stories = stories.select_related('author', 'author__profile')
    user = request.user
    form = HeraldSubmit(user=user)

    if request.method == 'POST':

        form = HeraldSubmit(data=request.POST, user=user)

        if form.is_valid():
            # Add the Link attribute.
            link = form.cleaned_data['url']
            text = form.cleaned_data['text']
            # Create the herald_list objects.
            herald = SharedLink.objects.create(author=user, text=text, url=link)

            return redirect(reverse('herald_list'))

    # Add pagination.
    context = dict(stories=stories, tab='herald_list', form=form)
    return render(request, 'herald/herald_base.html', context)


def herald_publish(request):

    if request.user.is_anonymous or not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You can not preform this action")
        return redirect(reverse('post_list'))

    post = herald_publisher()

    if settings.DEBUG:
        # TODO: DEBUG
        SharedLink.objects.update(status=SharedLink.ACCEPTED)

    if not post:
        messages.error(request, "Not enough submissions to publish.")
        return redirect(reverse('post_list'))

    return redirect(reverse('post_view', kwargs=dict(uid=post.uid)))