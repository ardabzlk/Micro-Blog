from bson import json_util
import json
from src.models.models import db


# ----------------------------------------------
# User collection


class users(db.Document):
    """
    User model for user collection
    user_id
    name
    surname
    """

    name = db.StringField(null=False, required=True, exists=True)
    surname = db.StringField(null=False, required=True, exists=True)
    username = db.StringField(null=False, required=True, exists=True)
    email = db.StringField(null=False, required=True, exists=True)
    password = db.StringField(null=False, required=True, exists=True)

    # to see the created user =>
    def to_json(self):
        bson_data = [{'user_id': self.id,
                      'name': self.name, 'surname': self.surname, 'username': self.username, 'email': self.email, 'password': self.password}]

        json_data_with_backslashes = json_util.dumps(bson_data)
        json_data = json.loads(json_data_with_backslashes)
        return json_data
# ----------------------------------------------


"""
# Example all fields model =>
# class AllFieldsModel(db.Document):
#     Meaningless Document with all field types.

#     binary_field = db.BinaryField()
#     boolean_field = db.BooleanField()
#     date_field = db.DateField()
#     date_time_field = db.DateTimeField()
#     decimal_field = db.DecimalField()
#     dict_field = db.DictField()
#     email_field = db.EmailField()
#     embedded_document_field = db.EmbeddedDocumentField(document_type=Embedded)
#     file_field = db.FileField()
#     float_field = db.FloatField()
#     int_field = db.IntField()
#     list_field = db.ListField(field=db.StringField)
#     reference_field = db.ReferenceField(document_type=Todo)
#     sorted_list_field = db.SortedListField(field=db.StringField)
#     string_field = db.StringField()
#     url_field = db.URLField()
#     cached_reference_field = db.CachedReferenceField(document_type=Todo)
#     complex_date_time_field = db.ComplexDateTimeField()
#     dynamic_field = db.DynamicField()
#     embedded_document_list_field = db.EmbeddedDocumentListField(
#         document_type=Embedded)
#     enum_field = db.EnumField(enum=[1, 2])
#     generic_embedded_document_field = db.GenericEmbeddedDocumentField()
#     generic_lazy_reference_field = db.GenericLazyReferenceField()
#     geo_json_base_field = db.GeoJsonBaseField()
#     geo_point_field = db.GeoPointField()
#     image_field = db.ImageField()
#     lazy_reference_field = db.LazyReferenceField(document_type=Todo)
#     line_string_field = db.LineStringField()
#     long_field = db.LongField()
#     map_field = db.MapField(field=db.StringField())
#     multi_line_string_field = db.MultiLineStringField()
#     multi_point_field = db.MultiPointField()
#     multi_polygon_field = db.MultiPolygonField()
#     point_field = db.PointField()
#     polygon_field = db.PolygonField()
#     sequence_field = db.SequenceField()
#     uuid_field = db.UUIDField()
#     generic_reference_field = db.GenericReferenceField(document_type=Todo)
#     object_id_field = db.ObjectIdField()
"""
