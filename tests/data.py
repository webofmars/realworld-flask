TAGS = ["mock-tag", "realworld"]

USER = {
    "email": "user@realworld.io",
    "token": "jwt.token.here",
    "username": "user",
    "bio": "I am a user.",
    "image": None,
}

AUTHOR = {
    "username": "user",
    "bio": "I am a user.",
    "image": None,
}

PROFILE = {
    "username": "user",
    "bio": "I am a user.",
    "image": None,
    "following": False,
}

COMMENT = {
    "id": 1,
    "createdAt": "2023-12-14T06:31:55.398685+00:00",
    "updatedAt": "2023-12-14T06:31:55.398685+00:00",
    "body": "What a nice article!",
    "author": PROFILE,
}

ARTICLE = {
    "slug": "how-to-article",
    "title": "How to Article",
    "description": "A test article.",
    "body": "This is just a test!",
    "tagList": ["test", "article"],
    "createdAt": "2023-12-14T06:31:55.398685+00:00",
    "updatedAt": "2023-12-14T06:31:55.398685+00:00",
    "favorited": True,
    "favoritesCount": 1,
    "author": PROFILE,
}
