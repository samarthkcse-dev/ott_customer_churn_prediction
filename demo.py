# import joblib

# encoder = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/label_encoders.pkl")

# print(type(encoder))
# print(encoder.keys())

# for column, values in encoder.items():
#     print("\nColumn:", column)
#     print(values)

# import joblib

# encoders = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/features.pkl")

# for column, encoder in encoders.items():
#     print("\nColumn:", column)
#     print("Classes:", encoder.classes_)

#     print("Mapping:")
#     for index, value in enumerate(encoder.classes_):
#         print(value, "=>", index)

import joblib

obj = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/features.pkl")

print(type(obj))
print(obj)