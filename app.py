
import re
from urllib.parse import urlparse, parse_qs

import streamlit as st


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Music Translator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================
# CUSTOM DESIGN
# =====================================

st.markdown("""
<style>

.stApp {
    background-color: #F7F8FC;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}

.main-header {
    text-align: center;
    padding: 25px 0 15px 0;
}

.main-header h1 {
    font-size: 42px;
    color: #26334A;
    font-weight: 800;
}

.main-header p {
    font-size: 16px;
    color: #788399;
}

.section-card {
    background: white;
    border-radius: 14px;
    padding: 22px;
    border: 1px solid #E5E8F0;
    margin-bottom: 18px;
}

.original-text {
    color: #26334A;
    font-size: 16px;
    line-height: 1.8;
}

.translated-text {
    color: #16836B;
    font-size: 15px;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #929AAA;
    font-size: 12px;
    padding: 30px;
}

</style>
""", unsafe_allow_html=True)


# =====================================
# SESSION STATE
# =====================================

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "checked_url" not in st.session_state:
    st.session_state.checked_url = None


# =====================================
# YOUTUBE URL VALIDATION
# =====================================

def extract_video_id(url):

    parsed = urlparse(url.strip())

    if parsed.hostname in ("youtube.com", "www.youtube.com",
                           "m.youtube.com", "music.youtube.com"):

        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]

        elif parsed.path.startswith(("/shorts/", "/embed/")):
            parts = parsed.path.strip("/").split("/")
            video_id = parts[1] if len(parts) > 1 else None

        else:
            video_id = None

    elif parsed.hostname in ("youtu.be", "www.youtu.be"):
        video_id = parsed.path.strip("/").split("/")[0]

    else:
        video_id = None

    if not video_id or not re.fullmatch(
        r"[A-Za-z0-9_-]{11}", video_id
    ):
        return None

    return video_id


# =====================================
# HEADER
# =====================================

st.markdown("""
<div class="main-header">
    <h1>🎵 Music Translator</h1>
    <p>
        Discover the meaning of music from around the world.
        <br>
        Original lyrics. Natural English translations.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# =====================================
# YOUTUBE INPUT
# =====================================

st.subheader("🎬 Enter your YouTube link")

youtube_url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed"
)

st.caption(
    "Paste a YouTube link to begin your translation."
)

if st.button(
    "Check YouTube link",
    type="primary",
    use_container_width=True
):

    video_id = extract_video_id(youtube_url)

    if video_id:

        st.session_state.video_id = video_id
        st.session_state.checked_url = youtube_url

        st.success("Valid YouTube link detected!")

    else:

        st.session_state.video_id = None
        st.session_state.checked_url = None

        st.error(
            "Invalid YouTube link. Please check your URL."
        )


# =====================================
# VIDEO PREVIEW
# =====================================

if st.session_state.video_id:

    st.divider()

    st.subheader("📺 Selected video")

    video_id = st.session_state.video_id

    st.video(
        f"https://www.youtube.com/watch?v={video_id}"
    )

    st.info(
        "Your YouTube link has been validated. "
        "Caption retrieval and translation will be "
        "connected in the next development phase."
    )


# =====================================
# TRANSLATION PREVIEW AREA
# =====================================

st.divider()

st.subheader("🌍 Translation preview")

left, right = st.columns(2)

with left:

    st.markdown("### Original lyrics")

    st.container(border=True).write(
        "Your original song lyrics will appear here."
    )

with right:

    st.markdown("### English translation")

    st.container(border=True).write(
        "Your English translation will appear here."
    )


# =====================================
# PDF SECTION
# =====================================

st.divider()

st.subheader("📄 Your translated song PDF")

st.write(
    "Once your translation is ready, "
    "you will be able to generate and download a PDF."
)


# =====================================
# FOOTER
# =====================================

st.markdown("""
<div class="footer">
    MUSIC TRANSLATOR · BUILT WITH PYTHON & STREAMLIT
</div>
""", unsafe_allow_html=True)
