from flask import request, jsonify
from server import app, db
from server.auth import get_or_create
from server.channel import Video
from server.user import User


@app.route('/api/follow', methods=['POST'])
def follow():
    params = request.get_json()
    access_token = params['access_token']
    user_to_follow = params['user_to_follow']
    user = get_or_create(access_token)
    to_follow = User.query.filter(User.id == user_to_follow).one()
    user.following.append(to_follow)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True
    })

@app.route('/api/unfollow', methods=['POST'])
def unfollow():
    params = request.get_json()
    access_token = params['access_token']
    user_to_unfollow = params['user_to_unfollow']
    user = get_or_create(access_token)
    to_unfollow = User.query.filter(User.id == user_to_unfollow).one()
    user.following.remove(to_unfollow)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True
    })



def simple_user_list(followers, page):
    base_resp = {
        'page': page,
        'total-pages': 1,
        'total-followers': len(followers)
    }

    if page != 1:
        return jsonify(dict(base_resp, error='Page not found')), 404

    follower_list = []
    for follower in followers:
        follower_list.append({
            'id': follower.id,
            'name': follower.name
        })
    return jsonify(dict(base_resp, followers=follower_list))


@app.route('/api/my-followers/')
@app.route('/api/my-followers/<int:page>')
def my_followers(page):
    """
    Currently using fake pagination
    """
    user = get_or_create(request.headers['access_token'])
    return simple_user_list(user.followers, page)


@app.route('/api/following/')
@app.route('/api/following/<int:page>')
def following(page):
    """
    Currently using fake pagination
    """
    user = get_or_create(request.headers['access_token'])
    return simple_user_list(user.following, page)

@app.route('/api/toggle-like/<int:video_id>')
def toggle_like(video_id):
    """
    Likes an video. If the the user already likes the video, it reverses the action.
    """
    user = get_or_create(request.headers['access_token'])
    video = Video.query.filter_by(id=video_id)

    user.liked_videos.append(video)
    db.session.commit()

    return jsonify({
        'success': True
    })

@app.route('/api/likes/<int:video_id>')
def likes(video_id):
    video = Video.query.filter_by(id=video_id).first()

    return jsonify({
        'likes': len(video.liking_users)
    })