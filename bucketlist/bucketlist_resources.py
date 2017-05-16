from flask import g, request, url_for
from flask_httpauth import HTTPTokenAuth
from flask_restful import reqparse, Resource, marshal
from sqlalchemy.orm.exc import NoResultFound

from . import db
from .models import User, BucketList, ListItems
from .serializer import bucketlists, bucketlistitems

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    """To validate the token sent by the user."""
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


parser = reqparse.RequestParser()


def _bucketlist(id):
    """Bucketlist owned by logged in user."""
    created_by = g.user
    bucketlist = db.session.query(BucketList).filter_by(
        id=id, created_by=created_by).first()
    if not bucketlist:
        # database result was required but none was found
        raise NoResultFound
    return bucketlist


def _bucketlist_item(item_id, id):
    """Check that a bucketlist item exists."""
    bucketlistitem = db.session.query(ListItems).filter_by(
        id=item_id, list_id=id).first()
    if not bucketlistitem:
        raise NoResultFound
    return bucketlistitem


def paginate(data, page, per_page):
    if not data:
        return {'Error': 'No records available'}, 400

    if data.has_prev:
        previous_url = ('http://' + request.host + url_for
                        (request.endpoint) + '?page=' + str(page - 1) +
                        '&per_page=' + str(per_page))
    else:
        previous_url = 'Null'

    if data.has_next:
        next_url = ('http://' + request.host + url_for
                    (request.endpoint) + '?page=' + str(page + 1) +
                    '&per_page=' + str(per_page))
    else:
        next_url = 'Null'

    return {'meta': {'previous_page': previous_url,
                     'next_page': next_url,
                     'total_pages': data.pages},
            'bucketlist': marshal(data.items, bucketlists)
            }, 200


class BucketListNew(Resource):
    """
        /v1/bucketlists/ endpoint
    """

    @auth.login_required
    def post(self):
        """
            Create a new bucketlist
        """
        parser.add_argument('list_name',
                            help='This field must be filled')
        arg = parser.parse_args()
        if arg['list_name']:
            list_name = arg['list_name']
        else:
            return {'message': 'Invalid entry.'}
        created_by = g.user
        existingbucketlist = db.session.query(BucketList).filter_by(
            list_name=list_name, created_by=created_by).first()
        if existingbucketlist:
            return {'message': 'Bucketlist  already exists'}, 400
        else:
            bucketlist = BucketList(list_name=list_name, created_by=created_by)
            db.session.add(bucketlist)
            db.session.commit()
            return marshal(bucketlist, bucketlists), 201

    @auth.login_required
    def get(self):
        """
            List all the created bucketlists
        """
        parser.add_argument('page')
        parser.add_argument('per_page')
        arg = parser.parse_args()
        page = arg['page']
        per_page = arg['per_page']
        if per_page > 100:
            per_page = 100
        word = request.args.get('q', None, type=str)

        created_by = g.user
        if created_by:
            if word:
                bucketlistget = BucketList.query.filter_by(
                    created_by=created_by).filter(
                        BucketList.list_name.ilike('%' + word + '%')).paginate(page, per_page, False)
                if list(bucketlistget) == []:
                    return {'message': 'Record containing {} cannot be found'.format(word)}, 404
                else:
                    return marshal(list(bucketlistget), bucketlists)

            else:
                bucketlistget = db.session.query(BucketList).filter_by(
                    created_by=created_by).paginate(page, per_page, False)
                return marshal(bucketlistget, bucketlists)

            if bucketlistget.has_prev:
                previous_url = ('http://' + request.host + url_for
                                (request.endpoint) + '?page=' + str(page - 1) +
                                '&per_page=' + str(per_page) +
                                '&q={}'.format(word))
            else:
                previous_url = 'Null'

            if bucketlistget.has_next:
                next_url = ('http://' + request.host + url_for
                            (request.endpoint) + '?page=' +
                            str(page + 1) + '&per_page=' + str(per_page) +
                            '&q={}'.format(word))
            else:
                next_url = 'Null'

            return {'meta': {'previous_page': previous_url,
                             'next_page': next_url,
                             'total_pages': bucketlistget.pages},
                    'bucketlist':
                        marshal(list(bucketlistget), bucketlists)
                    }, 200


class BucketListSingle(Resource):
    """
        /v1/bucketlists/<int:id> endpoint
    """

    @auth.login_required
    def get(self, id):
        """
            Get single bucketlist
        """
        try:
            bucketlist = _bucketlist(id)
            return marshal(bucketlist, bucketlists), 200
        except NoResultFound:
            return {'message': 'Bucketlist {} not found'.format(id)}, 404

    @auth.login_required
    def put(self, id):
        """
            Update single bucketlist
        """
        try:
            bucketlist = _bucketlist(id)
            parser.add_argument('list_name')
            arg = parser.parse_args()
            if arg['list_name']:
                bucketlist.list_name = arg['list_name']
            else:
                return {'message': 'Invalid Entry'}
            db.session.add(bucketlist)
            db.session.commit()
            return {'message': 'Bucketlist {} has been modified.'
                               .format(id)}, 202
        except NoResultFound:
            return {'message': 'Bucketlist {} does not exist.'
                               .format(id)}, 404

    @auth.login_required
    def delete(self, id):
        """
            Delete a single bucketlist
        """
        try:
            bucketlist = _bucketlist(id)
            db.session.delete(bucketlist)
            db.session.commit()
            return {'message': 'Bucketlist {}  deleted successfully.'
                               .format(id)}, 200
        except NoResultFound:
            return {'message': 'Bucketlist {} does not exist.'
                               .format(id)}, 404


class BucketListAddItem(Resource):
    """
        /v1/bucketlists/<int:id>/items/ endpoint
    """

    @auth.login_required
    def post(self, id):
        """
            Create a new item in bucket list
        """
        try:
            bucketlist = _bucketlist(id)
            print (bucketlist)
            # return bucketlist.id
            parser.add_argument('item_name')
            arg = parser.parse_args()
            if arg['item_name']:
                item = arg['item_name']
            else:
                return {'message': 'Invalid value passed.'}
            bucketlistitem = ListItems(bucketlist.id,
                                       item_name=item)
            db.session.add(bucketlistitem)
            db.session.commit()
            return {'message': '{0} has been added to Bucketlist {1}'
                               .format(item, id)}, 201
        except NoResultFound:
            return {'message': 'Bucketlist does not exist'}, 404


class BucketListEditItem(Resource):
    """
        /v1/bucketlists/<int:id>/item/<int:id> endpoint
    """
    @auth.login_required
    def get(self, id, item_id):
        """
            Get an item from bucketlist
        """
        try:
            bucketlistitem = _bucketlist_item(item_id, id)
            return marshal(bucketlistitem, bucketlistitems), 200
        except NoResultFound:
            return {'message': 'Item {} not found'.format(id)}, 404

    @auth.login_required
    def put(self, id, item_id):
        """
            Update a bucket list item
        """
        try:
            bucketlistitem = _bucketlist_item(item_id, id)
            parser.add_argument('item_name')
            parser.add_argument('done')
            arg = parser.parse_args()
            if arg['item_name']:
                bucketlistitem.item_name = arg['item_name']
            if arg['done']:
                bucketlistitem.done = arg['done']
            if not arg['item_name'] and not arg['done']:
                return {'message': 'Invalid value passed.'}
            db.session.add(bucketlistitem)
            db.session.commit()
            return {'message': 'Bucketlistitem {}  has been modified'
                               .format(item_id)}, 202
        except NoResultFound:
            return {'message': 'Bucketlist {0}, Item {1} has not been found'
                               .format(id, item_id)}, 404

    @auth.login_required
    def delete(self, id, item_id):
        """
            Delete an item in a bucket list
        """
        try:
            bucketlist = _bucketlist(id)
            if bucketlist:
                bucketlistitem = _bucketlist_item(item_id, id)
                db.session.delete(bucketlistitem)
                db.session.commit()
            return {'message': 'Item {}  deleted'
                    .format(item_id)}, 200
        except NoResultFound:
            return {'message': 'Item {} could not be found'
                    .format(item_id)}, 404
