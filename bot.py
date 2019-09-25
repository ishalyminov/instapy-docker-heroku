import time

from env_utils import env

from instapy import InstaPy, Settings

import proxy_api
import proxy_hack

PROXY = getattr(proxy_api, env('PROXY_TYPE'))()
TAGS_TO_FOLLOW = env('TAGS_TO_FOLLOW').split()

session = None

Settings.database_location = 'db/instapy.db'


def get_new_session():
    global session
    if session:
        session.end()
    session = InstaPy(username=env('INSTAGRAM_USERNAME'),
                      password=env('INSTAGRAM_PASSWORD'),
                      proxy_address=PROXY.proxy_host,
                      proxy_port=PROXY.proxy_port,
                      headless_browser=True,
                      geckodriver_path=env('GECKODRIVER_PATH'),
                      # nogui=True,
                      multi_logs=True,
                      disable_image_load=True)
    session.login()
    session.set_do_follow(enabled=True, percentage=int(env('FOLLOW_PERCENTAGE')))
    session.set_relationship_bounds(enabled=True,
                                    potency_ratio=None,
                                    delimit_by_numbers=True,
                                    max_followers=100000,
                                    max_following=3000,
                                    min_followers=100,
                                    min_following=100)
    """Image Check with Image tagging api"""
    # default enabled=False , enables the checking with the clarifai api (image tagging)
    # if secret and proj_id are not set, it will get the environment Variables
    # 'CLARIFAI_API_KEY'
    session.set_use_clarifai(enabled=False, api_key='xxx')
    session.set_dont_include(env('NEVER_UNFOLLOW_USERS', '').split())


while True:
    if PROXY.proxy_changed() or not session:
        get_new_session()
    sleep_time = int(env('SLEEP_TIME'))
    session.unfollow_users(amount=int(env('UNFOLLOW_NUMBER')),
                           nonFollowers=env('UNFOLLOW_ONLY_NON_FOLLOWERS', 'true') == 'true',
                           allFollowing=env('UNFOLLOW_ONLY_NON_FOLLOWERS', 'true') != 'true',
                           unfollow_after=48 * 60 * 60,
                           style='RANDOM',
                           sleep_delay=1800)

    print('Sleeping for {:.3f} seconds'.format(sleep_time))
    time.sleep(sleep_time)

    """Different tasks"""
    # you can put in as much tags as you want, likes 100 of each tag
    if PROXY.proxy_changed():
        get_new_session()
    session.like_by_tags(TAGS_TO_FOLLOW, amount=int(env('LIKE_BY_TAGS_AMOUNT', 0)))

    print('Sleeping for {:.3f} seconds'.format(sleep_time))
    time.sleep(sleep_time)

    """"Like by feed"""
    if PROXY.proxy_changed():
        get_new_session()
    # likes a given amount of posts on your feed, taking into account settings of commenting, like restrictions etc
    session.like_by_feed(amount=int(env('LIKE_BY_FEED_AMOUNT', 0)), randomize=True, interact=False)

    print('Sleeping for {:.3f} seconds'.format(sleep_time))
    time.sleep(sleep_time)

    if PROXY.proxy_changed():
        get_new_session()
    session.like_by_locations([env('LOCATION')], amount=int(env('LIKE_BY_LOCATION_AMOUNT', 0)))

    print('Sleeping for {:.3f} seconds'.format(sleep_time))
    time.sleep(sleep_time)

"""Ending the script"""
# clears all the cookies, deleting you password and all information from this session
session.end()
