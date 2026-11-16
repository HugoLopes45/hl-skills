import utils


def post_url(title):
    return "/posts/" + utils.slugify(title)
