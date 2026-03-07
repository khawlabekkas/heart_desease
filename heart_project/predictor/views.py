
from django.shortcuts import render, redirect
from django.http import JsonResponse
import joblib, os
import numpy as np
import pandas as pd
from .forms import HeartPredictionForm

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'heart_disease_model.pkl')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'heart.csv')

def load_or_train_model():
    if not os.path.exists(MODEL_PATH):
        # Train model if missing
        df = pd.read_csv(CSV_PATH)
        X = df.drop('target', axis=1)
        y = df['target']
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(class_weight='balanced')
        model.fit(X, y)
        joblib.dump(model, MODEL_PATH)
    return joblib.load(MODEL_PATH)

def home(request):
    return render(request, 'home.html')

def predict(request):
    model = load_or_train_model()
    predictions = None
    columns = None
    if request.method == 'POST':
        form = HeartPredictionForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['csv_file']:
                # Batch prediction
                csv_file = form.cleaned_data['csv_file']
                df = pd.read_csv(csv_file)
                columns = list(df.columns)
                preds = model.predict(df.values)
                predictions = [list(row) + [pred] for row, pred in zip(df.values, preds)]
                # Save batch predictions to recent_predictions.csv
                batch_df = df.copy()
                batch_df['prediction'] = preds
                batch_df.to_csv('recent_predictions.csv', mode='a', header=not os.path.exists('recent_predictions.csv'), index=False)
            else:
                # Single prediction
                features = [
                    form.cleaned_data['age'],
                    form.cleaned_data['sex'],
                    form.cleaned_data['cp'],
                    form.cleaned_data['trestbps'],
                    form.cleaned_data['chol'],
                    form.cleaned_data['fbs'],
                    form.cleaned_data['restecg'],
                    form.cleaned_data['thalach'],
                    form.cleaned_data['exang'],
                    form.cleaned_data['oldpeak'],
                    form.cleaned_data['slope'],
                    form.cleaned_data['ca'],
                    form.cleaned_data['thal'],
                ]
                pred = model.predict([features])[0]
                columns = ['Features']
                predictions = [[features, pred]]
                # Save manual prediction to recent_predictions.csv
                import csv
                with open('recent_predictions.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    if f.tell() == 0:
                        writer.writerow(['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','prediction'])
                    writer.writerow(features + [pred])
    else:
        form = HeartPredictionForm()
    return render(request, 'predict.html', {
        'form': form,
        'predictions': predictions,
        'columns': columns,
    })

def dashboard(request):
    # Load recent predictions from recent_predictions.csv (manual and batch)
    model = load_or_train_model()
    recent_predictions = []
    total = high_risk = low_risk = high_risk_percent = low_risk_percent = 0
    import csv
    if os.path.exists('recent_predictions.csv'):
        with open('recent_predictions.csv', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total = len(rows)
            high_risk = sum(int(row['prediction']) for row in rows)
            low_risk = total - high_risk
            high_risk_percent = round(100 * high_risk / total, 2) if total else 0
            low_risk_percent = round(100 * low_risk / total, 2) if total else 0
            # Show last 10 predictions
            for row in rows[-10:]:
                features = ', '.join(str(row[field]) for field in reader.fieldnames if field != 'prediction')
                risk = 'High' if int(row['prediction']) == 1 else 'Low'
                recent_predictions.append({'features': features, 'risk': risk})
    return render(request, 'dashboard.html', {
        'total_predictions': total,
        'high_risk_percent': high_risk_percent,
        'low_risk_percent': low_risk_percent,
        'recent_predictions': recent_predictions,
    })
