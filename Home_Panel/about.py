import streamlit as st


def show_about():

    st.markdown("""
    <style>

    .stApp {
        background:
            linear-gradient(120deg, rgba(3, 8, 20, 0.88), rgba(7, 22, 45, 0.76)),
            url("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    .about-shell {
        color: #f8fafc;
    }

    .about-hero {
        text-align: center;
        margin-bottom: 50px;
        padding: 40px 20px;
    }

    .about-kicker {
        width: fit-content;
        margin: 0 auto;
        padding: 8px 14px;
        border: 1px solid rgba(125, 211, 252, 0.34);
        border-radius: 999px;
        background: rgba(8, 47, 73, 0.46);
        color: #bae6fd;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0;
        margin-bottom: 18px;
        display: inline-block;
    }

    .about-main-title {
        color: #ffffff;
        font-size: 48px;
        line-height: 1.2;
        font-weight: 900;
        letter-spacing: -0.5px;
        margin: 0 0 16px 0;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    .about-subtitle {
        color: #dbeafe;
        font-size: 18px;
        line-height: 1.6;
        max-width: 750px;
        margin: 0 auto;
    }

    .section-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 900;
        margin: 40px 0 24px 0;
    }

    .section-card {
        border-radius: 0;
        border: none;
        background: transparent;
        padding: 0;
        margin: 40px 0;
        backdrop-filter: none;
        transition: none;
    }

    .section-card:hover {
        border: none;
        background: transparent;
        box-shadow: none;
    }

    .section-card h3 {
        color: #06b6d4;
        font-size: 28px;
        font-weight: 900;
        margin: 0 0 16px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(6, 182, 212, 0.3);
    }

    .section-desc {
        color: #cbd5e1;
        font-size: 16px;
        line-height: 1.8;
        margin-bottom: 24px;
    }

    .point-list {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin: 24px 0;
    }

    .point-item {
        display: flex;
        align-items: flex-start;
        padding: 0;
        border-radius: 0;
        background: transparent;
        border: none;
    }

    .point-item::before {
        content: "→";
        color: #06b6d4;
        font-weight: 900;
        font-size: 18px;
        margin-right: 12px;
        flex-shrink: 0;
    }

    .point-text {
        color: #dbeafe;
        font-size: 15px;
        font-weight: 500;
        line-height: 1.6;
    }

    .section-image {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .section-image img {
        width: 100%;
        height: 280px;
        object-fit: cover;
        display: block;
    }

    .highlight {
        color: #06b6d4;
        font-weight: 900;
    }

    @media (max-width: 900px) {
        .point-list {
            grid-template-columns: 1fr;
        }
        
        .about-main-title {
            font-size: 32px;
        }
        
        .section-title {
            font-size: 24px;
        }
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="about-shell">', unsafe_allow_html=True)

    st.markdown("""
    <div class="about-hero">
        <div class="about-kicker">ABOUT THIS PLATFORM</div>
        <div class="about-main-title">Airlines Customer Segmentation Analysis</div>
        <div class="about-subtitle">
            Transforming passenger data into actionable customer insights for airlines through advanced analytics and machine learning.
        </div>
    </div>
    """, unsafe_allow_html=True)

    def render_section(title, description, points, image_url, image_left=False):
        col_left, col_right = st.columns([1, 1])
        
        text_col = col_right if image_left else col_left
        img_col = col_left if image_left else col_right
        
        with text_col:
            points_html = "".join([f'<div class="point-item"><div class="point-text">{p}</div></div>' for p in points])
            st.markdown(f"""
            <div class="section-card">
                <h3>{title}</h3>
                <p class="section-desc">{description}</p>
                <div class="point-list">
                    {points_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with img_col:
            st.markdown(f"""
            <div class="section-image">
                <img src="{image_url}" alt="{title}">
            </div>
            """, unsafe_allow_html=True)

    render_section(
        "Customer Segmentation Analysis",
        "Analyze airline passengers and group them into meaningful customer segments based on their travel behavior, preferences, and loyalty patterns.",
        [
            "Customer Classification",
            "Travel Behavior Analysis",
            "Loyalty Insights",
            "Business Intelligence"
        ],
        "https://images.pexels.com/photos/62623/wing-plane-flying-airplane-62623.jpeg"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    render_section(
        "Data Science Lifecycle",
        "Customer data is processed through multiple stages before training machine learning models to ensure quality and relevance.",
        [
            "Data Collection",
            "Data Cleaning",
            "Feature Engineering",
            "PCA Transformation"
        ],
        "https://images.pexels.com/photos/669615/pexels-photo-669615.jpeg",
        image_left=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    render_section(
        "Machine Learning Model",
        "K-Means clustering identifies customer groups automatically by analyzing patterns in passenger data and behaviors.",
        [
            "K-Means Clustering",
            "Pattern Recognition",
            "Customer Profiling",
            "Model Evaluation"
        ],
        "https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    render_section(
        "Technologies Used",
        "Modern, industry-standard technologies power the analytics solution for reliability and performance.",
        [
            "Python",
            "Scikit-Learn",
            "Streamlit",
            "SQLite"
        ],
        "https://images.pexels.com/photos/577585/pexels-photo-577585.jpeg",
        image_left=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    render_section(
        "Business Benefits",
        "Airlines gain valuable customer insights and improve revenue through targeted strategies and personalized service.",
        [
            "Target Marketing",
            "Customer Retention",
            "Personalized Services",
            "Higher Profitability"
        ],
        "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg"
    )

    st.markdown('</div>', unsafe_allow_html=True)