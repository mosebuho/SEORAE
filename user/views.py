from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from user.decorators import login_required
from .forms import ChangeForm, RegisterForm, LoginForm
from .models import User
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
import json
from argon2 import PasswordHasher
import string, random

def register(request):
    register_form = RegisterForm()
    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-like_count")[:8]
    context = {"forms": register_form, "new_users": new_users, "hot_users": hot_users}

    if request.method == "GET":
        return render(request, "user/register.html", context)

    elif request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = User(
                user_id=register_form.user_id,
                user_pw=register_form.user_pw,
                user_name=register_form.user_name,
                user_email=register_form.user_email,
            )
            user.save()
            return redirect("/")
        else:
            context["forms"] = register_form
            if register_form.errors:
                for value in register_form.errors.values():
                    context["error"] = value
        return render(request, "user/register.html", context)


def login(request):
    loginform = LoginForm()
    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-like_count")[:8]
    context = {"forms": loginform, "new_users": new_users, "hot_users": hot_users}

    if request.method == "GET":
        return render(request, "user/login.html", context)

    elif request.method == "POST":
        loginform = LoginForm(request.POST)

        if loginform.is_valid():
            request.session["login_session"] = loginform.login_session
            request.session.set_expiry(0)
            return redirect("/")
        else:
            context["forms"] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context["error"] = value
        return render(request, "user/login.html", context)


def logout(request):
    request.session.flush()
    return redirect("/")


@login_required
def profile(request, pk):
    login_session = request.session.get("login_session", "")
    user = get_object_or_404(User, pk=pk)
    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-like_count")[:8]
    context = {
        "login_session": login_session,
        "user": user,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    return render(request, "user/profile.html", context)


@login_required
def myboard(request, pk):
    login_session = request.session.get("login_session", "")
    user = get_object_or_404(User, pk=pk)
    myboard = user.board_set.order_by("-id").all()
    page = request.GET.get("page", 1)
    paginator = Paginator(myboard, 10)
    boards = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-like_count")[:8]

    context = {
        "myboard": myboard,
        "boards": boards,
        "login_session": login_session,
        "user": user,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    return render(request, "user/myboard.html", context)


@login_required
def mycomment(request, pk):
    login_session = request.session.get("login_session", "")
    user = get_object_or_404(User, pk=pk)
    mycomment = user.comment_set.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(mycomment, 5)
    board_comments = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-like_count")[:8]

    context = {
        "login_session": login_session,
        "user": user,
        "mycomment": mycomment,
        "board_comments": board_comments,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    return render(request, "user/mycomment.html", context)


@login_required
def mylikeboard(request, pk):
    login_session = request.session.get("login_session", "")
    user = get_object_or_404(User, pk=pk)
    mylikeboard = user.like_boards.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(mylikeboard, 10)
    boards = paginator.page(page)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-like_count")[:8]

    context = {
        "mylikeboard": mylikeboard,
        "boards": boards,
        "login_session": login_session,
        "user": user,
        "new_users": new_users,
        "hot_users": hot_users,
    }
    return render(request, "user/mylikeboard.html", context)


@login_required
def mypwchange(request, pk):
    login_session = request.session.get("login_session", "")
    user = get_object_or_404(User, pk=pk)

    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-like_count")[:8]

    context = {
        "login_session": login_session,
        "user": user,
        "new_users": new_users,
        "hot_users": hot_users,
    }

    if user.id != login_session:
        return redirect(f"/user/profile/{pk}/")

    if request.method == "GET":
        write_form = ChangeForm(instance=user)
        context["forms"] = write_form
        return render(request, "user/mypwchange.html", context)

    elif request.method == "POST":
        write_form = ChangeForm(request.POST)

        if write_form.is_valid():
            user.user_pw = write_form.user_pw
            user.save()
            return redirect(f"/user/profile/{pk}/")
        else:
            context["forms"] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context["error"] = value
                return render(request, "user/mypwchange.html", context)


@login_required
def name_edit(request, pk):
    login_session = request.session.get("login_session")
    target_user = User.objects.get(pk=pk)
    user_id = login_session
    if login_session == target_user.id:
        data = {
            "user_id": user_id,
            "name": target_user.user_name,
        }
        return HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
        )


@login_required
def name_edit_done(request, pk):
    login_session = request.session.get("login_session")
    target_user = User.objects.get(pk=pk)
    user_id = login_session
    edit_name = request.POST.get("edit_name")
    if login_session == target_user.id:
        if edit_name:
            target_user.user_name = edit_name
            target_user.save()
            data = {
                "user_id": user_id,
                "edit_name": edit_name,
            }
            return HttpResponse(
                json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
            )


@login_required
def user_quit(request, pk):
    login_session = request.session.get("login_session")
    user = get_object_or_404(User, pk=pk)
    if login_session == user.id:
        user.delete()
        request.session.flush()
        return redirect("/")


def findmyid(request):
    users = User.objects.all()
    new_users = users.order_by("-id")[:8]
    hot_users = users.order_by("-like_count")[:8]
    context = {"new_users": new_users, "hot_users": hot_users}
    return render(request, "user/findmyid.html", context)


def findmyid_done(request):
    user_email = request.POST.get("user_email")
    user = User.objects.get(user_email=user_email)
    if user_email:
        new_pw_len = 12
        password = string.ascii_letters + string.digits + string.punctuation 
        new_pw = ""
        for i in range(new_pw_len):
            new_pw += random.choice(password)
        user.user_pw = PasswordHasher().hash(new_pw)
        user.save()
        data = {
            "user_email": user_email,
        }
        title = "아이디/비밀번호 정보"
        content = f"""
        요청하신 계정 정보는 다음과 같습니다.\n\n
        아이디    :  {user.user_id}
        이메일    :  {user.user_email}
        닉네임    :  {user.user_name}
        가입일    :  {user.user_register_dttm}
        임시 비밀번호 :  {new_pw}
        \n 임시 비밀번호는 해킹의 위험이 있으니 반드시 로그인 후 비밀번호를 변경해주세요.
        사이트 바로 가기:http://127.0.0.1:8000/home
        """
        mail = EmailMessage(title, content, to=[user_email])
        mail.send()
    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )
