PROGRAMME = (
        ('B.Tech', 'B.Tech'),
        ('B.S', 'B.S'),
        ('BS-MBA', 'BS-MBA'),
        ('BS-MS', 'BS-MS'),
        ('BS-MT', 'BS-MT'),
        ('BT-M.Des', 'BT-M.Des'),
        ('BT-MBA', 'BT-MBA'),
        ('BT-MS', 'BT-MS'),
        ('Exchng Prog.', 'Exchng Prog.'),
        ('MBA', 'MBA'),
        ('MDes', 'MDes'),
        ('MS-Research', 'MS-Research'),
        ('MSc(2 yr)', 'MSc(2 yr)'),
        ('MSc(Int)', 'MSc(Int)'),
        ('MT(Dual)', 'MT(Dual)'),
        ('MTech', 'MTech'),
        ('PGPEX-VLM', 'PGPEX-VLM'),
        ('PhD', 'PhD'),
        ('PhD(Dual)', 'PhD(Dual)'),
        ('Prep.', 'Prep.'),
        ('SURGE', 'SURGE')
)

DEPT = (
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
        ('Earth Sciences', 'ES'),
        ('Cognitive Sciences', 'Cognitive Sciences'),
        ('Humanities and Social Sciences', 'HSS'),
        ('Laser Technology', 'Laser Technology'),
        ('Photonics Science & Engineering', 'Photonics Science & Engg.'),
        ('Statistics', 'Statistics')
)

YEAR = (
        ('Y16', 'Y16'),
        ('Y15', 'Y15'),
        ('Y14', 'Y14'),
        ('Y13', 'Y13'),
        ('Y12', 'Y12'),
        ('Y11', 'Y11'),
)

HALL = (
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
        ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'),
)

NOMI_STATUS = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
)

INTERVIEW_STATUS = (
        ('Interview Not Done', 'Interview Not Done'),
        ('Interview Done', 'Interview Done'),
)

STATUS = (
        ('Nomination created', 'Nomination created'),
        ('Nomination out', 'Nomination out'),
        ('Interview period', 'Interview period'),
        ('Interview period and Reopening initiated','Interview period and Reopening initiated'),
        ('Interview period and Nomination reopened', 'Interview period and Nomination reopened'),
        ('Sent for ratification', 'Sent for ratification'),
        ('Work done', 'Work done'),
)

GROUP_STATUS = (

        ('normal', 'normal'),
        ('grouped', 'grouped')
)

G_STATUS = (
        ('created', 'created'),
        ('out', 'out')
)

CLUB_STATUS = (
        ('Club created', 'Club created'),
        ('Club approved', 'Club approved'),

)

POST_STATUS = (
        ('Post created', 'Post created'),
        ('Post approved', 'Post approved'),
)

POST_PERMS = (
        ("normal", "normal"),
        ("can ratify the post", "can ratify the post"),
        ("can approve post and send nominations to users", "can approve post and send nominations to users"),
)

TAG_PERMS = (
        ('normal', 'normal'),
        ('Can create', 'Can create'),
)

HALL_1 = (
        ('All', 'All'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
        ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'),
)

DEPT_1 = (
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
        ('Earth Sciences', 'ES'),
        ('Cognitive Sciences', 'Cognitive Sciences'),
        ('Humanities and Social Sciences', 'HSS'),
        ('Laser Technology', 'Laser Technology'),
        ('Photonics Science & Engineering', 'Photonics Science & Engg.'),
        ('Statistics', 'Statistics')
)

YEAR_1 = (
        ('All', 'All'),
        ('Y16', 'Y16'),
        ('Y15', 'Y15'),
        ('Y14', 'Y14'),
        ('Y13', 'Y13'),
        ('Y12', 'Y12'),
        ('Y11', 'Y11'),
)

SESSION_CHOICES = (
        (2017, 2017),
        (2018, 2018),
)

DERATIFICATION = (
    ('end tenure', 'end tenure'),
    ('remove from post', 'remove from post'),
    ('deratified', 'deratified'),
    ('removed', 'removed'),

)