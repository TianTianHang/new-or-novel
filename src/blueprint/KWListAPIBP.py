from flask import Blueprint


from blueprint.apiclass import KWListAPI

kwlist_bp = Blueprint('kwlist', __name__)
kwlist_view = KWListAPI.as_view('kwlist')
kwlist_bp.add_url_rule('/api/kwlist/', view_func=kwlist_view,
                       methods=['GET'])
kwlist_bp.add_url_rule('/api/kwlist/<string:kw_id>/', view_func=kwlist_view,
                       methods=['GET', 'DELETE'])
kwlist_bp.add_url_rule('/api/kwlist/', view_func=kwlist_view, methods=['POST', 'PUT'])

