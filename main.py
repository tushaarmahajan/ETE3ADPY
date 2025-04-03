import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from PIL import Image, ImageFilter
import os

# 🌟 Set Beautiful Theme & Layout
st.set_page_config(page_title="CHRISPO '25 Analysis", page_icon="🏆", layout="wide")

# 🎯 Generate Dataset Function
def generate_dataset():
    np.random.seed(42)
    sports = ["Football", "Basketball", "Tennis", "Badminton", "Cricket", 
              "Volleyball", "Hockey", "Table Tennis", "Swimming", "Athletics"]
    colleges = ["College A", "College B", "College C", "College D", "College E"]
    states = ["Karnataka", "Tamil Nadu", "Kerala", "Maharashtra", "Telangana"]
    
    data = {
        "Participant_ID": range(1, 301),
        "Name": [f"Player {i}" for i in range(1, 301)],
        "Sport": np.random.choice(sports, 300),
        "College": np.random.choice(colleges, 300),
        "State": np.random.choice(states, 300),
        "Day": np.random.randint(1, 6, 300),
        "Age": np.random.randint(18, 30, 300),
        "Gender": np.random.choice(["Male", "Female", "Other"], 300),
        "Score": np.random.randint(1, 100, 300),
        "Feedback": np.random.choice(["Great event!", "Loved it!", "Needs improvement!", "Amazing experience!"], 300),
    }

    df = pd.DataFrame(data)
    df.to_csv("participants.csv", index=False)
    return df

# 📊 Load Dataset
if not os.path.exists("participants.csv"):
    df = generate_dataset()
else:
    df = pd.read_csv("participants.csv")

# 🎛️ Sidebar Controls
st.sidebar.header("🎯 Controls")

# 🛠️ Generate New Dataset Button
if st.sidebar.button("🔄 Generate New Dataset"):
    df = generate_dataset()
    st.sidebar.success("✅ New dataset generated!")

# 🎚️ Data Filters
selected_sport = st.sidebar.selectbox("Select Sport", ["All"] + list(df["Sport"].unique()))
selected_college = st.sidebar.selectbox("Select College", ["All"] + list(df["College"].unique()))
selected_state = st.sidebar.selectbox("Select State", ["All"] + list(df["State"].unique()))

# 🔍 Apply Filters
filtered_df = df.copy()
if selected_sport != "All":
    filtered_df = filtered_df[filtered_df["Sport"] == selected_sport]
if selected_college != "All":
    filtered_df = filtered_df[filtered_df["College"] == selected_college]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]

# 🏆 App Title
st.title("🏆 CHRISPO '25 Tournament Analysis by TUSHAR MAHAJAN of 3 MCA A (2447156)")

st.write("### 📊 Filtered Participation Data")
st.dataframe(filtered_df)

# 📈 Participation Trends
st.write("## 📈 Participation Trends")

# 🎨 Modern Colors
sns.set_palette("coolwarm")

# 1️⃣ Bar Chart: Sports-wise Participation
st.write("### 🎯 Sports-wise Participation")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.countplot(x="Sport", data=df, order=df["Sport"].value_counts().index, ax=ax1, palette="pastel")
ax1.set_title("Sports-wise Participation")
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

# 2️⃣ Line Chart: Day-wise Participation
st.write("### 📅 Day-wise Participation")
daywise_count = df["Day"].value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(daywise_count.index, daywise_count.values, marker='o', linestyle='-', color='#007bff', linewidth=2)
ax2.set_title("Participation Trend Over Days", fontsize=14, color="#007bff")
ax2.set_xlabel("Day", fontsize=12)
ax2.set_ylabel("Number of Participants", fontsize=12)
st.pyplot(fig2)

# 3️⃣ Pie Chart: College-wise Participation
st.write("### 🎓 College-wise Participation")
college_counts = df["College"].value_counts()
fig3, ax3 = plt.subplots(figsize=(6, 6))
ax3.pie(college_counts, labels=college_counts.index, autopct='%1.1f%%', colors=sns.color_palette("coolwarm", len(college_counts)))
ax3.set_title("College-wise Participation Distribution", fontsize=14, color="#d9534f")
st.pyplot(fig3)

# 4️⃣ Histogram: Age Distribution
st.write("### 🎂 Age Distribution of Participants")
fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.histplot(df["Age"], bins=10, kde=True, color="purple", alpha=0.7)
ax4.set_title("Age Distribution of Participants", fontsize=14, color="purple")
ax4.set_xlabel("Age", fontsize=12)
ax4.set_ylabel("Count", fontsize=12)
st.pyplot(fig4)

# 5️⃣ Box Plot: Score Distribution by Sport
st.write("### 🏅 Score Distribution by Sport")
fig5, ax5 = plt.subplots(figsize=(8, 4))
sns.boxplot(x="Sport", y="Score", data=df, palette="muted")
ax5.set_title("Score Distribution Across Sports", fontsize=14, color="#17a2b8")
ax5.tick_params(axis='x', rotation=45)
st.pyplot(fig5)

# 🌟 Word Cloud with Filters
st.write("## 💬 Participant Feedback - Word Cloud")

# 🎯 Sidebar Filters for Word Cloud
selected_wc_sport = st.sidebar.selectbox("Filter Word Cloud by Sport", ["All"] + list(df["Sport"].unique()), key="wc_sport")
selected_wc_college = st.sidebar.selectbox("Filter Word Cloud by College", ["All"] + list(df["College"].unique()), key="wc_college")
selected_wc_state = st.sidebar.selectbox("Filter Word Cloud by State", ["All"] + list(df["State"].unique()), key="wc_state")

# 📊 Apply Word Cloud Filters
filtered_wc_df = df.copy()
if selected_wc_sport != "All":
    filtered_wc_df = filtered_wc_df[filtered_wc_df["Sport"] == selected_wc_sport]
if selected_wc_college != "All":
    filtered_wc_df = filtered_wc_df[filtered_wc_df["College"] == selected_wc_college]
if selected_wc_state != "All":
    filtered_wc_df = filtered_wc_df[filtered_wc_df["State"] == selected_wc_state]

# 🔠 Generate Word Cloud
if not filtered_wc_df.empty:
    all_feedback = " ".join(filtered_wc_df["Feedback"])
    wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="coolwarm").generate(all_feedback)
    fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)
else:
    st.warning("No feedback available for the selected filters.")

# 🖼️ Image Processing from "images" Folder
st.write("## 🖼️ Image Processing")

# Check if "images" folder exists
image_folder = "images"
if not os.path.exists(image_folder):
    st.error("❌ 'images' folder not found! Please create an 'images' folder and add some images.")
else:
    # Get list of images from folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(("jpg", "png", "jpeg"))]
    
    if image_files:
        # User selects an image
        selected_image = st.selectbox("Choose an Image", image_files)

        # Load and display the selected image
        image_path = os.path.join(image_folder, selected_image)
        image = Image.open(image_path)
        st.image(image, caption="Original Image", use_column_width=True)

        # 🔄 Image Filters
        filter_option = st.radio("Choose an Image Filter", ["Original", "Grayscale", "Blur", "Sharpen"])

        if filter_option == "Grayscale":
            image = image.convert("L")
        elif filter_option == "Blur":
            image = image.filter(ImageFilter.BLUR)
        elif filter_option == "Sharpen":
            image = image.filter(ImageFilter.SHARPEN)

        st.image(image, caption="Processed Image", use_column_width=True)
    else:
        st.warning("⚠️ No images found in 'images' folder. Please add some images.")


# 🎯 Summary
st.write("### 🎯 Summary")
st.write("- The dashboard provides insights into sports participation trends.")
st.write("- Word Cloud gives an overview of participant feedback.")
st.write("- Image processing module allows viewing and modifying sports-related images.")

st.success("✅ CHRISPO '25 Analysis Completed Successfully!")
