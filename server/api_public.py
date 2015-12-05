"""
This file contains all requests that are to be used by
the end user. Examples include searching for channels and
videos
"""

from flask import jsonify
from server import app, db
from server.channel import Video, Channel
from server.user import User
from server.util import get_video_url


@app.route('/api/channels/')
@app.route('/api/channels/<int:page>')
def list_channels(page=1):
    """
    A paginated listing of all channels
    """
    pagination = Channel.query.paginate(page, error_out=False)

    # Base response will always be used as the base, even if
    # the request fails
    base_resp = {
        'page': page,
        'total-pages': pagination.pages,
        'total-channels': pagination.total
    }

    if len(pagination.items) == 0 and page != 1:
        return jsonify(dict(base_resp, error='Page not found')), 404

    channel_list = []
    for channel in pagination.items:
        channel_list.append({
            'channel': channel.name,
            'slug': channel.slug,
            'url': channel.url
        })
    return jsonify(dict(base_resp, channels=channel_list))

@app.route('/api/channel/<int:id>')
def channel_by_url(id):
    ch = Channel.query.filter_by(id=id).first()

    return jsonify({
        'channel': ch.name,
        'slug': ch.slug,
        'url': ch.url,
        'hosted-by': ch.hosted_by
    })


@app.route('/api/videos/')
@app.route('/api/videos/<int:page>')
def list_videos(page=1):
    """
    A paginated listing of all videos
    """
    pagination = Video.query.paginate(page, 5, error_out=False)

    # Base response will always be used as the base, even if
    # the request fails
    base_resp = {
        'page': page,
        'total-pages': pagination.pages,
        'total-videos': pagination.total
    }

    if len(pagination.items) == 0 and page != 1:
        return jsonify(dict(base_resp, error='Page not found')), 404

    video_list = []
    for video in pagination.items:
        video_list.append({
            'video': video.name,
            'slug': video.slug,
            'channel-id': video.channel_id,
            'channel-name': video.channel.name,
            'url': get_video_url(video),
            'video-id': video.id
        })
    return jsonify(dict(base_resp, videos=video_list))


@app.route('/api/users/<string:query>/')
@app.route('/api/users/<string:query>/<int:page>')
def list_users(query, page=1):
    """
    A paginated search for users by name
    """
    pagination = User.query.filter(User.name.ilike("%" + query + "%")).paginate(page, error_out=False)

    # Base response will always be used as the base, even if
    # the request fails
    base_resp = {
        'page': page,
        'total-pages': pagination.pages,
        'total-users': pagination.total
    }

    if len(pagination.items) == 0 and page != 1:
        return jsonify(dict(base_resp, error='Page not found')), 404

    user_list = []
    for user in pagination.items:
        user_list.append({
            'id': user.id,
            'name': user.name
        })
    return jsonify(dict(base_resp, users=user_list))
