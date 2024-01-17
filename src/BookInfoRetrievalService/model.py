import marshmallow as mm

class BookCompletionQuery(mm.Schema):
    partial = mm.fields.String()

class BookCompletionResponse(mm.Schema):
    completions = mm.fields.List(mm.fields.String())

class BookInfoQuery(mm.Schema):
    title = mm.fields.String()

class BookInfoResponse(mm.Schema):
    book_id = mm.fields.Integer()
    name = mm.fields.String()
    cover = mm.fields.String()
    url = mm.fields.String()
    authors = mm.fields.List(mm.fields.String())
    rating = mm.fields.Float()
    created_editions = mm.fields.Integer()
    year = mm.fields.Integer()