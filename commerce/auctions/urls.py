from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:id>", views.view_listing, name="listing"),
    path("listing/<int:id>/bid/", views.place_bid_view, name="bid"),
    path("listing/<int:id>/close/", views.close_listing_view, name="close"),
    path("listing/<int:id>/watchlist/", views.modify_watchlist_view, name="modify_watchlist"),
    path("watchlist/", views.watchlist_view, name="view_watchlist"),
    path("listing/<int:id>/comment/", views.add_comment_view, name="comment"),
    path("categories/", views.categories_view, name="categories"),
    path("category/<str:category_name>", views.category_view, name="category")
]
