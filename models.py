import peewee as pw

db = pw.MySQLDatabase('library', user='root',
                      password='root', host='localhost', port=3306)


class MySQLModel(pw.Model):
    """Base class for all Peewee models using a MySQL database."""

    class Meta:
        """
        Metadata for the MySQLModel model.
        This class specifies the database connection to be used for this model.
        """
        database = db


class Books(MySQLModel):
    """ Books model for storing Books-related information """

    bookID = pw.CharField(unique=True)
    title = pw.CharField()
    authors = pw.CharField()
    average_rating = pw.FloatField()
    isbn = pw.CharField(unique=True)
    isbn13 = pw.CharField(unique=True)
    language_code = pw.CharField()
    num_pages = pw.IntegerField()
    ratings_count = pw.IntegerField()
    text_reviews_count = pw.IntegerField()
    publication_date = pw.DateField()
    publisher = pw.CharField()

    class Meta:
        db_table = 'Books'


class Users(MySQLModel):
    """ Users model for storing all users information """

    username = pw.CharField(unique=True)
    created_date = pw.DateTimeField(constraints=[pw.SQL('DEFAULT CURRENT_TIMESTAMP')])
    status = pw.BooleanField(default=True)
    email = pw.CharField(unique=True)
    role = pw.CharField(default="default")
    permissions = pw.TextField(default="{'r':'home'}")
    pw_hash = pw.CharField()

    class Meta:
        db_table = 'Users'


if __name__ == "__main__":
    # Books.truncate_table()
    # db.drop_tables([Books])
    # db.create_tables([Books])
    pass
