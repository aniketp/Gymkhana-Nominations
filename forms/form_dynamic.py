from django import forms


class NominationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(NominationForm, self).__init__(*args, **kwargs)

        for i, values in enumerate(extra):
            label, klass, field_args,ques_id = values
            self.fields['%s' % ques_id] = klass(label=label, **field_args)
