from django import forms

HALL = (
    (0, 'All'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
    (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

DEPT = (
        ('All', 'All'),
        ('Aerospace Engineering', 'AE'),
        ('Biological Sciences & Engineering', 'BSBE'),
        ('Chemical Engineering', 'CHE'),
        ('Civil Engineering', 'CE'),
        ('Computer Science & Engineering', 'CSE'),
        ('Electrical Engineering', 'EE'),
        ('Materials Science & Engineering', 'MSE'),
        ('Mechanical Engineering', 'ME'),
        ('Industrial & Management Engineering', 'IME'),
        ('Chemistry', 'CHM'),
        ('Mathematics & Scientific Computing', 'MTH'),
        ('Physics', 'PHY'),
        ('Earth Sciences', 'ES')
    )

YEAR = (
        ('All', 'All'),
        ('Y16', 'Y16'),
        ('Y15', 'Y15'),
        ('Y14', 'Y14'),
        ('Y13', 'Y13'),
        ('Y12', 'Y12'),
        ('Y11', 'Y11'),
    )


class NominationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    year = forms.ChoiceField(choices=YEAR, label="Batch", initial='All', widget=forms.Select(), required=True)
    department = forms.ChoiceField(choices=DEPT, label="Dept", initial='All', widget=forms.Select(), required=True)
    hall = forms.ChoiceField(choices=HALL, label="Hall", initial=0, widget=forms.Select(), required=True)


class PostForm(forms.Form):
    # club_name = forms.CharField()
    post_title = forms.CharField()





