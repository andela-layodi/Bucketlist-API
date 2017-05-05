from flask import g, request
from flask_httpauth import HTTPTokenAuth
from flask_restful import reqparse, Resource, marshal
from sqlalchemy.orm.exc import NoResultFound

from . import db
from .models import User, BucketList, ListItems
from .serializer import bucketlists

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


def _bucketlist(list_id):
    """Bucketlist owned by logged in user."""
    created_by = g.user
    bucketlist = db.session.query(BucketList).filter_by(
        id=list_id, created_by=created_by).first()
    if not bucketlist:
        # database result was required but none was found
        raise NoResultFound
    return bucketlist


def _bucketlist_item(item_id, list_id):
    """Check that a bucketlist item exists."""
    bucketlistitem = db.session.query(ListItems).filter_by(
        id=item_id, list_id=list_id).first()
    if not bucketlistitem:
        raise NoResultFound
    return bucketlistitem


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
        q = request.args.get('q', None, type=str)

        created_by = g.user
        if created_by:
            if q:
                bucketlistget = BucketList.query.filter_by(
                    created_by=created_by).filter(
                        BucketList.list_name.ilike('%' + q + '%'))
                return marshal(list(bucketlistget), bucketlists)
            else:
                bucketlistget = db.session.query(BucketList).filter_by(
                    created_by=created_by).all()
                return marshal(bucketlistget, bucketlists)


class BucketListSingle(Resource):
    """
        /v1/bucketlists/<int:id> endpoint
    """

    @auth.login_required
    def get(self, list_id):
        """
            Get single bucketlist
        """
        try:
            bucketlist = _bucketlist(list_id)
            return marshal(bucketlist, bucketlists), 200
        except NoResultFound:
            return {'message': 'Bucketlist {} not found'.format(list_id)}, 404

    @auth.login_required
    def put(self, list_id):
        """
            Update single bucketlist
        """
        try:
            bucketlist = _bucketlist(list_id)
            parser.add_argument('list_name')
            arg = parser.parse_args()
            if arg['list_name']:
                bucketlist.list_name = arg['list_name']
            else:
                return {'message': 'Invalid Entry'}
            db.session.add(bucketlist)
            db.session.commit()
            return {'message': 'Bucketlist {} has been modified.'
                               .format(list_id)}, 202
        except NoResultFound:
            return {'message': 'Bucketlist {} does not exist.'
                               .format(list_id)}, 404

    @auth.login_required
    def delete(self, list_id):
        """
            Delete a single bucketlist
        """
        try:
            bucketlist = _bucketlist(list_id)
            db.session.delete(bucketlist)
            db.session.commit()
            return {'message': 'Bucketlist {}  deleted successfully.'
                               .format(list_id)}, 200
        except NoResultFound:
            return {'message': 'Bucketlist {} does not exist.'
                               .format(list_id)}, 404


class BucketListAddItem(Resource):
    """
        /v1/bucketlists/<int:id>/items/ endpoint
    """

    @auth.login_required
    def post(self, list_id):
        """
            Create a new item in bucket list
        """
        try:
            bucketlist = _bucketlist(list_id)
            # return bucketlist.id
            parser.add_argument('item_name')
            arg = parser.parse_args()
            if arg['item_name']:
                item = arg['item_name']
            else:
                return {'message': 'Invalid value passed.'}
            bucketlistitem = ListItems(
                item_name=item, list_id=bucketlist.id)
            db.session.add(bucketlistitem)
            db.session.commit()
            return {'message': '{0} has been added to Bucketlist {1}'
                               .format(item, list_id)}, 201
        except NoResultFound:
            return {'message': 'Bucketlist does not exist'}, 404


class BucketListEditItem(Resource):
    """
        /v1/bucketlists/<int:id>/item/<int:id> endpoint
    """

    @auth.login_required
    def put(self, list_id, item_id):
        """
            Update a bucket list item
        """
        try:
            bucketlistitem = _bucketlist_item(item_id, list_id)
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
                               .format(list_id, item_id)}, 404

    @auth.login_required
    def delete(self, list_id, item_id):
        """
            Delete an item in a bucket list
        """
        try:
            bucketlist = _bucketlist(list_id)
            if bucketlist:
                bucketlistitem = _bucketlist_item(item_id, list_id)
                db.session.delete(bucketlistitem)
                db.session.commit()
            return {'message': 'Item {}  deleted'
                    .format(item_id)}, 200
        except NoResultFound:
            return {'message': 'Item {} could not be found'
                    .format(item_id)}, 404
