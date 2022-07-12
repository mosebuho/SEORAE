from django.shortcuts import render
from board.models import Board
from user.models import User


def home(request):
    login_session = request.session.get("login_session")
    board = Board.objects.all()
    recipe = Board.objects.filter(board_name="recipe")
    
    new_board = board.order_by("-id")[:14]
    hot_board = board.order_by("-like_count")[:14]
    new_recipe = recipe.order_by("-id")[:14]
    hot_recipe = recipe.order_by("-like_count")[:14]

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-point")[:8]
    context = {
        "new_board": new_board,
        "hot_board": hot_board,
        "new_recipe": new_recipe,
        "hot_recipe": hot_recipe,
        "login_session": login_session,
        "new_users":new_users,
        "hot_users":hot_users,
    }
    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user
    return render(request, "home/index.html", context)


def search(request):
    login_session = request.session.get("login_session")
    boards = Board.objects.all().order_by("-id")

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-point")[:8]

    q = request.POST.get("q", "")
    context = {"login_session": login_session, "q": q, "new_users":new_users, "hot_users":hot_users}
    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user
    if q:
        boards = boards.filter(title__icontains=q)
        context["boards"] = boards
        return render(request, "home/search.html", context)
    else:
        return render(request, "home/search.html", context)
