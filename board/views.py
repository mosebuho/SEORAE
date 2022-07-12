from django.shortcuts import render, redirect
from .forms import BoardWriteForm
from .models import Board, Comment
from user.models import User
from user.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder


def all(request):
    login_session = request.session.get("login_session")

    all_boards = Board.objects.order_by("-id")
    page = request.GET.get("page", 1)
    paginator = Paginator(all_boards, 15)
    boards = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]

    context = {
        "all_boards": all_boards,
        "boards": boards,
        "login_session": login_session,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user
    return render(request, "board/all.html", context)


def free(request):
    login_session = request.session.get("login_session")

    free_boards = Board.objects.filter(board_name="free").order_by("-id")
    page = request.GET.get("page", 1)
    paginator = Paginator(free_boards, 15)
    boards = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]

    context = {
        "free_boards": free_boards,
        "boards": boards,
        "login_session": login_session,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user
    return render(request, "board/free.html", context)


def recipe(request):
    login_session = request.session.get("login_session")

    recipe_boards = Board.objects.filter(board_name="recipe").order_by("-id")
    page = request.GET.get("page", 1)
    paginator = Paginator(recipe_boards, 15)
    boards = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]

    context = {
        "recipe_boards": recipe_boards,
        "boards": boards,
        "login_session": login_session,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user
    return render(request, "board/recipe.html", context)


def hoogie(request):
    login_session = request.session.get("login_session")

    hoogie_boards = Board.objects.filter(board_name="hoogie").order_by("-id")
    page = request.GET.get("page", 1)
    paginator = Paginator(hoogie_boards, 15)
    boards = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]

    context = {
        "hoogie_boards": hoogie_boards,
        "boards": boards,
        "login_session": login_session,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user
    return render(request, "board/hoogie.html", context)


def question(request):
    login_session = request.session.get("login_session")

    question_boards = Board.objects.filter(board_name="question").order_by("-id")
    page = request.GET.get("page", 1)
    paginator = Paginator(question_boards, 15)
    boards = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]

    context = {
        "question_boards": question_boards,
        "boards": boards,
        "login_session": login_session,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user
    return render(request, "board/question.html", context)


def notice(request):
    login_session = request.session.get("login_session")

    notice_boards = Board.objects.filter(board_name="notice").order_by("-id")
    page = request.GET.get("page", 1)
    paginator = Paginator(notice_boards, 15)
    boards = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]

    context = {
        "notice_boards": notice_boards,
        "boards": boards,
        "login_session": login_session,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user
    return render(request, "board/notice.html", context)


@login_required
def write(request):
    login_session = request.session.get("login_session")
    user = User.objects.get(id=login_session)
    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]

    context = {
        "login_session": login_session,
        "user": user,
        "new_users": new_users,
        "hot_users": hot_users,
    }

    if request.method == "GET":
        write_form = BoardWriteForm()
        context["forms"] = write_form
        return render(request, "board/write.html", context)

    elif request.method == "POST":
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(id=login_session)
            board = Board(
                title=write_form.title,
                contents=write_form.contents,
                writer=writer,
                board_name=write_form.board_name,
            )
            board.save()
            user.point += 2
            user.save()
            return redirect(f"/board/detail/{board.id}/")
        else:
            context["forms"] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context["error"] = value
            return render(request, "board/write.html", context)


def detail(request, pk):
    login_session = request.session.get("login_session")
    board = get_object_or_404(Board, id=pk)
    comments = board.comment_set.all()

    page = request.GET.get("page", 1)
    paginator = Paginator(comments, 8)
    board_comments = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]

    context = {
        "board": board,
        "board_comments": board_comments,
        "login_session": login_session,
        "new_users": new_users,
        "hot_users": hot_users,
    }

    if login_session:
        user = User.objects.get(pk=login_session)
        context["user"] = user

    if board.writer.user_id == login_session:
        context["writer"] = True
    else:
        context["writer"] = False

    response = render(request, "board/detail.html", context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get("hitboard", "_")

    if f"_{pk}_" not in cookie_value:
        cookie_value += f"{pk}_"
        response.set_cookie(
            "hitboard", value=cookie_value, max_age=max_age, httponly=True
        )
        board.hits += 1
        board.save()
    return response


@login_required
def delete(request, pk):
    login_session = request.session.get("login_session")
    board = get_object_or_404(Board, id=pk)
    if board.writer.id == login_session:
        board.delete()
        return redirect("/")
    else:
        return redirect(f"/board/detail/{pk}/")


@login_required
def update(request, pk):
    login_session = request.session.get("login_session")
    user = User.objects.get(id=login_session)
    board = get_object_or_404(Board, pk=pk)
    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("point")[:8]
    context = {
        "login_session": login_session,
        "user": user,
        "board": board,
        "new_users": new_users,
        "hot_users": hot_users,
    }

    if board.writer.id != login_session:
        return redirect(f"/board/detail/{pk}/")

    if request.method == "GET":
        write_form = BoardWriteForm(instance=board)
        context["forms"] = write_form
        return render(request, "board/update.html", context)

    elif request.method == "POST":
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            board.title = write_form.title
            board.contents = write_form.contents
            board.board_name = write_form.board_name
            board.save()
            return redirect(f"/board/detail/{board.id}/")
        else:
            context["forms"] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context["error"] = value
                return render(request, "board/update.html", context)


@login_required
def comment_write(request, pk):
    login_session = request.session.get("login_session")
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.get(id=login_session)
    content = request.POST.get("content")
    if content:
        comment = Comment.objects.create(
            board=board,
            content=content,
            writer=user,
        )
        board.save()
        user.point += 1
        user.save()
        data = {
            "writer": user.user_name,
            "content": content,
            "created_at": comment.created_string,
            "comment_id": comment.id,
            "comment_count": board.comment_set.count(),
        }
        if user == board.writer:
            data["self_comment"] = "(글쓴이)"

        return HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
        )


@login_required
def comment_update(request, pk):
    login_session = request.session.get("login_session")
    comment_id = request.POST.get("comment_id")
    target_comment = Comment.objects.get(pk=comment_id)
    if login_session == target_comment.writer.id:
        data = {
            "comment_id": comment_id,
            "content": target_comment.content,
        }
        return HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
        )


@login_required
def comment_update_done(request, pk):
    login_session = request.session.get("login_session")
    board = get_object_or_404(Board, id=pk)
    comment_id = request.POST.get("comment_id")
    target_comment = Comment.objects.get(pk=comment_id)
    edit_content = request.POST.get("edit_content")
    if login_session == target_comment.writer.id:
        if edit_content:
            target_comment.content = edit_content
            target_comment.save()
            board.save()
            data = {
                "comment_id": comment_id,
                "edit_content": edit_content,
            }
            return HttpResponse(
                json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
            )


@login_required
def comment_delete(request, pk):
    login_session = request.session.get("login_session")
    board = get_object_or_404(Board, id=pk)
    comment_id = request.POST.get("comment_id")
    target_comment = Comment.objects.get(pk=comment_id)

    if login_session == target_comment.writer.id:
        target_comment.deleted = True
        target_comment.save()
        board.save()
        data = {
            "comment_id": comment_id,
        }
        return HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
        )


def like(request):
    login_session = request.session.get("login_session")
    board_id = request.GET["board_id"]
    board = Board.objects.get(id=board_id)
    writer = User.objects.get(id=board.writer_id)

    if board.like.filter(id=login_session).exists():
        board.like.remove(login_session)
        message = "취소"
        if login_session:
            board.like_count -= 1
            writer.like_count -= 1
            writer.point -= 1
            writer.save()
            board.save()
    elif not login_session:
        message = "비로그인"
    else:
        board.like.add(login_session)
        message = "추천"
        if login_session:
            writer.like_count += 1
            writer.point += 1
            board.like_count += 1
            writer.save()
            board.save()
    data = {"like_count": board.like_count, "message": message}
    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )
