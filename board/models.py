from django.db import models
from datetime import datetime, timedelta, timezone


class Board(models.Model):
    title = models.CharField(max_length=64, verbose_name="글 제목")
    contents = models.TextField(verbose_name="글 내용")
    writer = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, verbose_name="작성자"
    )
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name="글 작성일")
    board_name = models.CharField(max_length=32, verbose_name="게시판 종류")
    update_dttm = models.DateTimeField(auto_now=True, verbose_name="마지막 수정일")
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like = models.ManyToManyField("user.User", related_name="like_boards", blank=True)
    like_count = models.PositiveIntegerField(default=0, verbose_name="추천수")

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.write_dttm
        if time < timedelta(minutes=1):
            return "방금 전"
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + "분 전"
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + "시간 전"
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.write_dttm.date()
            return str(time.days) + "일 전"
        else:
            return self.write_dttm.strftime("%m/%d")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "board"
        verbose_name = "게시판"
        verbose_name_plural = "게시판"


class Comment(models.Model):
    board = models.ForeignKey(
        Board, null=True, blank=True, on_delete=models.CASCADE, verbose_name="게시글"
    )
    writer = models.ForeignKey(
        "user.User", on_delete=models.SET_NULL, null=True, verbose_name="작성자"
    )
    content = models.CharField(max_length=2000, verbose_name="댓글 내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    deleted = models.BooleanField(default=False, verbose_name="삭제 여부")

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at
        if time < timedelta(minutes=1):
            return "방금 전"
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + "분 전"
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + "시간 전"
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + "일 전"
        else:
            return self.created_at.strftime("%m/%d")

    def __str__(self):
        return self.content

    class Meta:
        db_table = "comment"
        verbose_name = "댓글"
        verbose_name_plural = "댓글"
