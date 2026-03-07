from django import forms

class HeartPredictionForm(forms.Form):
    age = forms.IntegerField(label='Age', min_value=1, max_value=120)
    sex = forms.ChoiceField(label='Sex', choices=[(1, 'Male'), (0, 'Female')])
    cp = forms.ChoiceField(label='Chest Pain Type', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2'), (3, 'Type 3')])
    trestbps = forms.IntegerField(label='Resting Blood Pressure')
    chol = forms.IntegerField(label='Cholesterol')
    fbs = forms.ChoiceField(label='Fasting Blood Sugar > 120 mg/dl', choices=[(1, 'True'), (0, 'False')])
    restecg = forms.ChoiceField(label='Resting ECG', choices=[(0, 'Normal'), (1, 'Abnormal'), (2, 'Hypertrophy')])
    thalach = forms.IntegerField(label='Max Heart Rate')
    exang = forms.ChoiceField(label='Exercise Induced Angina', choices=[(1, 'Yes'), (0, 'No')])
    oldpeak = forms.FloatField(label='ST Depression')
    slope = forms.ChoiceField(label='Slope of Peak', choices=[(0, 'Upsloping'), (1, 'Flat'), (2, 'Downsloping')])
    ca = forms.IntegerField(label='Number of Major Vessels', min_value=0, max_value=4)
    thal = forms.ChoiceField(label='Thalassemia', choices=[(1, 'Normal'), (2, 'Fixed Defect'), (3, 'Reversible Defect')])
    csv_file = forms.FileField(label='Batch CSV Upload', required=False)
