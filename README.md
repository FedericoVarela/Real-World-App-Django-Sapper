# Real World Django + Sapper App

## Requirements
 - Authenticate users via JWT (login/signup pages + logout button on settings page)
 - CRU* users (sign up & settings page - no deleting required)
 - CRUD Articles
 - CR*D Comments on articles (no updating required)
 - GET and display paginated lists of articles
 - Favorite articles
 - Follow other users

## Frontend Specs
Using the hosted API
Simply point your API requests to https://conduit.productionready.io/api and you're good to go!

Unit test(s)
Include at least one unit test in your repo to demonstrate how testing works (full testing coverage is not required!)

## Routing Guidelines
 - Home page (URL: /#/ )
 - List of tags
 - List of articles pulled from either Feed, Global, or by Tag
 - Pagination for list of articles
 - Sign in/Sign up pages (URL: /#/login, /#/register )
 - Uses JWT (store the token in localStorage)
 - Authentication can be easily switched to session/cookie based
 - Settings page (URL: /#/settings )
 - Editor page to create/edit articles (URL: /#/editor, /#/editor/article-slug-here )
 - Article page (URL: /#/article/article-slug-here )
 - Delete article button (only shown to article's author)
 - Render markdown from server client side
 - Comments section at bottom of page
 - Delete comment button (only shown to comment's author)
 - Profile page (URL: /#/profile/:username, /#/profile/:username/favorites )
 - Show basic user info
 - List of articles populated from author's created articles or author's favorited articles
 - Backend Specs
 - All backend implementations need to adhere to our API spec.

Unit test(s)
Include at least one unit test in your repo to demonstrate how testing works (full testing coverage is not required!)