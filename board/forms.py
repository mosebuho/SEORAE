from django import forms
from .models import Board
from django_summernote.widgets import SummernoteWidget
from django_summernote.fields import SummernoteTextField


class BoardWriteForm(forms.ModelForm):
    title = forms.CharField(
        label="글 제목",
        widget=forms.TextInput(attrs={"placeholder": "게시글 제목"}),
        required=True,
    )

    contents = SummernoteTextField()

    options = (
        ("free", "자유 게시판"),
        ("recipe", "레시피 게시판"),
        ("hoogie", "후기 게시판"),
        ("question", "문의 게시판"),
    )

    board_name = forms.ChoiceField(
        label="게시판 선택", widget=forms.Select(), choices=options
    )

    field_order = ["title", "board_name", "contents"]

    class Meta:
        model = Board
        fields = ["title", "contents", "board_name"]
        widgets = {"contents": SummernoteWidget()}

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title", "")
        contents = cleaned_data.get("contents", "")
        board_name = cleaned_data.get("board_name", "")

        if title == "":
            self.add_error("title", "글 제목을 입력해주세요.")
        elif contents == "":
            self.add_error("contents", "글 내용을 입력해주세요.")
        elif board_name == "":
            self.add_error("contents", "게시판 종류를 선택해주세요.")
        else:
            self.title = title
            self.contents = contents
            self.board_name = board_name