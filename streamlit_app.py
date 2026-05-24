import streamlit as st

import os

st.title("Driver Drowsiness Detection System")

st.write("AI based Driver Monitoring System")
st.write("Press 'Q' to close the camera window")
# Start Button

if st.button("Start Detection"):
    st.success("Driver Detection Started")
    st.success("Camera access works only in local system.")
    os.system("python appdd.py")


#info
st.info("This system detects driver drowsiness using AI.")

# Features
st.write("""
Features:
- Eye Closure Detection
- Head Pose Detection
- Alarm Alertimg = frame.to_ndarray(format="bgr24")

- Screenshot Capture
""")

# GitHub Link
st.markdown("[GitHub Repository](https://github.com/Vishnuvardhan-54/Driver-Drowsiness-Detection.git)")