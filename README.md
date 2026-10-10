# Smart Car Health Predictor

AI-powered car health checker built for the Maruti Suzuki Innovation Challenge
(Domain: Automotive AI & Vehicle Intelligence).

## What it does
Enter your car details and get a health score (0-100), the part most at risk,
and a plain-language service advice.

## Features
- Input form: car age, km driven, km since service, driving style
- Random Forest model predicts health score and risky part
- Green / yellow / red health label
- Indian conditions: traffic, rough roads and monsoon inputs
- Cost saver: fix now vs ignore it
- "Why this result?" chart
- English, Hindi and Bengali
- One-click WhatsApp service reminder

## How to run
'''
pip install streamlit scikit-learn pandas matplotlib
python make_data.py
python train_model.py
python -m streamlit run app.py
'''


## Note
The model is trained on simulated data based on common wear patterns.
With real service records, it can be retrained for higher accuracy.

## Team
- Samadrita Ghosh
- Aruna De
- Snehil Raj Singh

