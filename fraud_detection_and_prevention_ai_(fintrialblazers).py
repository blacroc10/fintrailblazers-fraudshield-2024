# -*- coding: utf-8 -*-
"""Fraud Detection and Prevention AI (FinTrialblazers).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1T9m3QIrfcG92glE-uF9MYVt8bd5AxhrX

Importing all the necessary libraries
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from imblearn.under_sampling import RandomUnderSampler
import matplotlib.pyplot as plt
import seaborn as sns
import logging

#loading dataset using pandas

credit_card_data=pd.read_csv('/content/creditcard.csv')

credit_card_data.info()

credit_card_data.isnull().sum()

"""Removing rows where values are NaN"""

credit_card_data.dropna(inplace=True)

credit_card_data.isnull().sum()

print("Missing values after dropping NaNs:")
credit_card_data.isnull()

credit_card_data['Class'].value_counts()

legit=credit_card_data[credit_card_data.Class==0]
fraud=credit_card_data[credit_card_data.Class==1]

print("Legitimate transactions statistics:")
print(legit.Amount.describe())
print("\nFraudulent transactions statistics:")
print(fraud.Amount.describe())

legit.Amount.describe()

fraud.Amount.describe()

credit_card_data.groupby('Class').mean()

n = len(fraud)
print(f'The value of n is: {n}')

legit_sample=legit.sample(n)

new_dataset=pd.concat([legit_sample,fraud],axis=0)

new_dataset['Class'].value_counts()

new_dataset.groupby('Class').mean()

x=new_dataset.drop(columns='Class',axis=1)
y=new_dataset['Class']

print(x)

print(y)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,stratify=y,random_state=2)

model=LogisticRegression(random_state=2)

model.fit(x_train,y_train)

y_train_pred = model.predict(x_train)
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f"Training accuracy: {train_accuracy:.4f}")

y_test_pred = model.predict(x_test)
test_accuracy = accuracy_score(y_test, y_test_pred)
print(f"Test accuracy: {test_accuracy:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_test_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred))

sns.heatmap(confusion_matrix(y_test, y_test_pred), annot=True, cmap='Blues', fmt='g')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

y_test_pred_proba = model.predict_proba(x_test)[:, 1]

threshold = 0.5  # Adjust this threshold as needed
y_test_pred_adjusted = (y_test_pred_proba >= threshold).astype(int)

print("\nAdjusted Confusion Matrix:")
print(confusion_matrix(y_test, y_test_pred_adjusted))
print("\nAdjusted Classification Report:")
print(classification_report(y_test, y_test_pred_adjusted))

logging.basicConfig(filename='fraud_detection.log', level=logging.INFO)

def notify_fraud_team(transaction_id, amount):
    print(f"Notifying fraud detection team: Fraud detected in Transaction ID {transaction_id}, Amount {amount}")

def block_transaction(transaction_id):
    print(f"Blocking transaction: Transaction ID {transaction_id}")

fraudulent_transactions = []
fraudulent_transactions_info = []
for idx, (pred_prob, true_class, amount) in enumerate(zip(y_test_pred_proba, y_test, x_test['Amount'])):
    if pred_prob >= threshold:
        transaction_id = idx  # Example: Using transaction index as transaction ID (replace with actual ID from dataset)
        fraudulent_transactions.append(transaction_id)
        fraudulent_transactions_info.append({
            'Transaction ID': transaction_id,
            'Probability': pred_prob,
            'Amount': amount
        })
        notify_fraud_team(transaction_id, amount)
        block_transaction(transaction_id)
        logging.info(f"Fraud detected: Probability {pred_prob:.4f}, True Class {true_class}, Amount {amount}")

fraudulent_transactions_df = pd.DataFrame(fraudulent_transactions_info)
print("Predicted Fraudulent Transactions:\n", fraudulent_transactions_df)

total_transactions = len(y_test)
num_fraudulent_transactions = len(fraudulent_transactions)
fraud_percentage = (num_fraudulent_transactions / total_transactions) * 100
non_fraud_percentage = 100 - fraud_percentage

fraud_data = [fraud_percentage, non_fraud_percentage]
labels = ['Fraudulent Transactions', 'Non-Fraudulent Transactions']

plt.figure(figsize=(8, 8))
plt.pie(fraud_data, labels=labels, autopct='%1.1f%%', startangle=90, colors=['red', 'green'])
plt.title('Percentage of Fraudulent Transactions')
plt.show()