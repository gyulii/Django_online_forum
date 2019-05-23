from functools import wraps, partial

from django.http import JsonResponse
from django.utils.decorators import available_attrs
from ratelimit.decorators import ratelimit

from biostar.forum import auth
from biostar.forum.models import Post, Vote


def ajax_msg(msg, status, **kwargs):
    payload = dict(status=status, msg=msg)
    payload.update(kwargs)
    return JsonResponse(payload)


ajax_success = partial(ajax_msg, status='success')
ajax_error = partial(ajax_msg, status='error')


class ajax_error_wrapper:
    """
    Used as decorator to trap/display  errors in the ajax calls
    """

    def __init__(self, method):
        self.method = method

    def __call__(self, func, *args, **kwargs):

        @wraps(func, assigned=available_attrs(func))
        def _ajax_view(request, *args, **kwargs):

            if request.method != self.method:
                return ajax_error(f'{self.method} method must be used.')

            if not request.user.is_authenticated:
                return ajax_error('You must be logged in.')

            return func(request, *args, **kwargs)

        return _ajax_view


def ajax_test(request):
    """
    Creates a commment on a top level post.
    """
    msg="OK"
    print (f"HeRe= {request.POST} ")
    return ajax_error(msg=msg)


@ratelimit(key='ip', rate='50/h')
@ratelimit(key='ip', rate='10/m')
@ajax_error_wrapper(method="POST")
def ajax_vote(request):
    was_limited = getattr(request, 'limited', False)

    if was_limited:
        return ajax_error(msg="Too many votes from same IP address. Temporary ban.")

    user = request.user
    type_map = dict(upvote=Vote.UP, bookmark=Vote.BOOKMARK, accept=Vote.ACCEPT)

    vote_type = request.POST.get('vote_type')
    vote_type = type_map.get(vote_type)
    post_uid = request.POST.get('post_uid')

    # Check the post that is voted on.
    post = Post.objects.filter(uid=post_uid).first()

    if post.author == user and vote_type == Vote.UP:
        return ajax_error("You can not upvote your own post.")

    if post.author == user and vote_type == Vote.ACCEPT:
        return ajax_error("You can not accept your own post.")

    if post.root.author != user and vote_type == Vote.ACCEPT:
        return ajax_error("Only the person asking the question may accept this answer.")

    msg, vote, change = auth.apply_vote(post=post, user=user, vote_type=vote_type)

    return ajax_success(msg=msg, change=change)


@ajax_error_wrapper(method="POST")
def ajax_subs(request):
    was_limited = getattr(request, 'limited', False)

    if was_limited:
        return ajax_error(msg="Too many votes from same IP address. Temporary ban.")

    post_uid = ""
    1/0
    return


