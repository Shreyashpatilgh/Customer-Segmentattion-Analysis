import streamlit as st

from src.config import APP_TITLE


def add_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                linear-gradient(120deg, rgba(3, 8, 20, 0.88), rgba(7, 22, 45, 0.76)),
                url("https://images.unsplash.com/photo-1464037866556-6812c9d1c72e?q=80&w=1920&auto=format&fit=crop");
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

        .home-shell {
            color: #f8fafc;
        }

        .hero-wrap {
            min-height: 520px;
            display: grid;
            grid-template-columns: 1fr;
            gap: 34px;
            align-items: center;
            margin-top: 6px;
            margin-bottom: 34px;
        }

        .hero-kicker {
            width: fit-content;
            padding: 8px 14px;
            border: 1px solid rgba(125, 211, 252, 0.34);
            border-radius: 999px;
            background: rgba(8, 47, 73, 0.46);
            color: #bae6fd;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0;
            margin-bottom: 18px;
        }

        .hero-title {
            color: #ffffff;
            font-size: 58px;
            line-height: 1.02;
            font-weight: 900;
            letter-spacing: 0;
            margin: 0 0 20px 0;
            max-width: 760px;
        }

        .hero-copy {
            color: #dbeafe;
            font-size: 18px;
            line-height: 1.75;
            max-width: 690px;
            margin-bottom: 26px;
        }

        .hero-actions {
            display: none;
        }

        .home-proof {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            max-width: 650px;
        }

        .proof-item {
            padding: 14px 16px;
            border-radius: 14px;
            background: rgba(15, 23, 42, 0.58);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .proof-value {
            color: #7dd3fc;
            font-size: 22px;
            font-weight: 900;
            line-height: 1.1;
        }

        .proof-label {
            color: #cbd5e1;
            font-size: 13px;
            margin-top: 5px;
        }

        .command-panel {
            position: relative;
            min-height: 430px;
            border-radius: 28px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.15);
            background:
                linear-gradient(160deg, rgba(15, 23, 42, 0.78), rgba(14, 116, 144, 0.24)),
                url("https://images.unsplash.com/photo-1540962351504-03099e0a754b?q=80&w=1200&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            box-shadow: 0 22px 70px rgba(0, 0, 0, 0.34);
        }

        .panel-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(2, 6, 23, 0.12), rgba(2, 6, 23, 0.82));
        }

        .flight-card {
            position: absolute;
            left: 24px;
            right: 24px;
            bottom: 24px;
            padding: 22px;
            border-radius: 18px;
            background: rgba(2, 6, 23, 0.76);
            border: 1px solid rgba(255, 255, 255, 0.13);
            backdrop-filter: blur(10px);
        }

        .flight-card h3 {
            color: #ffffff !important;
            font-size: 22px;
            margin: 0 0 12px 0;
        }

        .route-row {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 14px;
            align-items: center;
            margin: 18px 0;
        }

        .airport-code {
            color: #ffffff;
            font-size: 32px;
            font-weight: 900;
        }

        .airport-label {
            color: #cbd5e1;
            font-size: 12px;
            margin-top: 3px;
        }

        .route-line {
            height: 2px;
            min-width: 110px;
            background: linear-gradient(90deg, #38bdf8, #22c55e);
            border-radius: 999px;
        }

        .signal-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }

        .signal-box {
            padding: 12px;
            border-radius: 12px;
            background: rgba(15, 23, 42, 0.82);
        }

        .signal-box strong {
            display: block;
            color: #ffffff;
            font-size: 15px;
        }

        .signal-box span {
            color: #a7f3d0;
            font-size: 12px;
        }

        .section-title {
            color: #ffffff;
            font-size: 30px;
            font-weight: 900;
            margin: 30px 0 8px 0;
        }

        .section-copy {
            color: #cbd5e1;
            font-size: 16px;
            line-height: 1.7;
            max-width: 780px;
            margin-bottom: 22px;
        }

        .workflow {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
            margin-bottom: 34px;
        }

        .step {
            min-height: 150px;
            padding: 20px;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.66);
            border: 1px solid rgba(255, 255, 255, 0.11);
        }

        .step-number {
            color: #67e8f9;
            font-size: 14px;
            font-weight: 900;
            margin-bottom: 12px;
        }

        .step-title {
            color: #ffffff;
            font-size: 18px;
            font-weight: 850;
            margin-bottom: 8px;
        }

        .step-copy {
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.55;
        }

        .module-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
        }

        .module-card {
            min-height: 230px;
            overflow: hidden;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(15, 23, 42, 0.7);
        }

        .module-image {
            height: 108px;
            background-size: cover;
            background-position: center;
        }

        .module-body {
            padding: 18px;
        }

        .module-title {
            color: #ffffff;
            font-size: 18px;
            font-weight: 850;
            margin-bottom: 8px;
        }

        .module-desc {
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.55;
        }

        .st-key-home_primary_cta button,
        .st-key-home_secondary_cta button {
            display: none !important;
        }

        @media (max-width: 900px) {
            .hero-wrap,
            .workflow,
            .module-grid {
                grid-template-columns: 1fr;
            }

            .home-proof {
                grid-template-columns: 1fr;
            }

            .hero-actions {
                grid-template-columns: 1fr;
            }

            .hero-title {
                font-size: 40px;
            }

            .command-panel {
                min-height: 380px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_home():
    add_bg()

    st.markdown('<div class="home-shell">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero-wrap">
            <div>
                <div class="hero-kicker">AIRLINE INTELLIGENCE PLATFORM</div>
                <h1 class="hero-title">{APP_TITLE}</h1>
                <div class="hero-copy">
                    Turn passenger behavior into precise customer segments, reveal loyalty
                    patterns, and help teams personalize airline experiences with confidence.
                </div>
                <div class="home-proof">
                    <div class="proof-item">
                        <div class="proof-value">129K+</div>
                        <div class="proof-label">Passenger records analyzed</div>
                    </div>
                    <div class="proof-item">
                        <div class="proof-value">4</div>
                        <div class="proof-label">Actionable customer segments</div>
                    </div>
                    <div class="proof-item">
                        <div class="proof-value">95%</div>
                        <div class="proof-label">Model accuracy target</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-title">From Raw Passenger Data To Clear Decisions</div>
        <div class="section-copy">
            The app guides airline teams from exploration to prediction with a practical
            workflow built around customer behavior, model performance, and usable reports.
        </div>
        <div class="workflow">
            <div class="step">
                <div class="step-number">01</div>
                <div class="step-title">Explore</div>
                <div class="step-copy">Filter, scan, and understand passenger data before modeling.</div>
            </div>
            <div class="step">
                <div class="step-number">02</div>
                <div class="step-title">Segment</div>
                <div class="step-copy">Use clustering to group travelers by behavior and service needs.</div>
            </div>
            <div class="step">
                <div class="step-number">03</div>
                <div class="step-title">Predict</div>
                <div class="step-copy">Classify new customers into the most relevant segment instantly.</div>
            </div>
            <div class="step">
                <div class="step-number">04</div>
                <div class="step-title">Act</div>
                <div class="step-copy">Export insights for support, marketing, loyalty, and operations.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    modules = [
        (
            "Data Explorer",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1200&auto=format&fit=crop",
            "Interactive filters, charts, and quick reads for airline customer data.",
        ),
        (
            "Model Performance",
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1200&auto=format&fit=crop",
            "Evaluate clustering quality, PCA views, and model behavior in one place.",
        ),
        (
            "Customer Prediction",
            "https://images.unsplash.com/photo-1529070538774-1843cb3265df?q=80&w=1200&auto=format&fit=crop",
            "Predict the segment of a new passenger from profile and travel details.",
        ),
        (
            "Cluster Insights",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1200&auto=format&fit=crop",
            "Translate segment patterns into clear operational and customer insights.",
        ),
        (
            "Auto Analyzer",
            "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1200&auto=format&fit=crop",
            "Surface smart findings quickly for exploratory analysis and reporting.",
        ),
        (
            "Download Results",
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=1200&auto=format&fit=crop",
            "Export segmented datasets and reports for stakeholders.",
        ),
    ]

    module_cards = ""
    for title, image, desc in modules:
        module_cards += f"""
<div class="module-card">
    <div class="module-image" style="background-image: url({image});"></div>
    <div class="module-body">
        <div class="module-title">{title}</div>
        <div class="module-desc">{desc}</div>
    </div>
</div>
"""

    st.markdown(
        f"""
<div class="section-title">Core Modules</div>
<div class="module-grid">
{module_cards}
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)
