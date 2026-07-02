import streamlit as st
import requests
import os

# --- CONFIGURATION ---
BASE_URL = os.getenv("API_URL", "http://skeptiscan_api:8000").rstrip("/")
API_URL = f"{BASE_URL}/api/v1" if not BASE_URL.endswith("/api/v1") else BASE_URL

st.set_page_config(
    page_title="Skepti-Scan | The AI Skeptic", 
    page_icon="🤨", 
    layout="wide" # Changed to wide to give the tabs more breathing room
)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/bottts/svg?seed=Skeptic&backgroundColor=transparent", width=100)
    st.title("Skepti-Scan")
    st.caption("Trust nothing. Verify everything.")
    st.divider()
    
    # 1. The Team Expander
    with st.expander("👨‍💻 The Team", expanded=True):
        st.markdown("### Ziyad Ahmed")
        st.markdown("*Junior AI Engineer*")
        st.markdown("- Architecting robust & scalable backend systems")
        st.markdown("- [Connect on LinkedIn](https://www.linkedin.com/in/ziyadalawami/)")
        
        st.markdown("---")
        
        st.markdown("### Yousef Tarek")
        st.markdown("*Junior AI Engineer*")
        st.markdown("- Designing intelligent RAG & pipeline logic")
        st.markdown("- [Connect on LinkedIn](https://www.linkedin.com/in/yousef-tarek-fathy/)")

    st.divider()
    
    # 2. About the Project Expander
    with st.expander("🕵️ About the Project"):
        st.markdown("""
        **Why Skepti-Scan?**
        * **We Assume You're Lying:** An AI tool built on the premise that raw claims without sources are useless.
        * **Live RAG Pipeline:** We don't rely on hallucinated LLM memories. We cross-reference claims against live web data.
        * **Cold, Hard JSON:** Structured outputs meant for serious database ingestion, not just chatbots.
        """)

# --- MAIN PAGE ---
st.title("🤨 The Skeptic's Desk")
st.markdown("*Your ruthlessly analytical AI fact-checker. Submit your claims below.*")
st.divider()

# --- TABS LAYOUT ---
tab_investigate, tab_log = st.tabs(["🔍 Investigate", "📂 Investigation Log"])

# TAB 1: Investigation Form
with tab_investigate:
    # Dropdown for Future Batch Processing
    ingest_mode = st.selectbox(
        "Select Investigation Mode:", 
        ["Single Claim", "Batch Processing"]
    )
    
    if ingest_mode == "Single Claim":
        with st.form("claim_form"):
            claim_text = st.text_area(
                "Enter a claim, quote, or alleged fact:", 
                placeholder="e.g., The Great Wall of China is visible from space without aid."
            )
            submitted = st.form_submit_button("🔍 Scrutinize Claim")

        if submitted:
            if not claim_text.strip():
                st.error("I cannot investigate silence. Please enter a specific claim.")
            else:
                with st.spinner("Cross-referencing internal and live web data... 🕵️‍♂️"):
                    try:
                        response = requests.post(f"{API_URL}/verify", json={"claim_text": claim_text})
                        
                        if response.status_code == 201:
                            data = response.json()
                            status = data['status']
                            confidence_pct = (data['confidence'] or 0.0) * 100
                            
                            st.subheader("The Verdict")
                            
                            if status == "verified":
                                st.success(f"### ✅ VERIFIED\n**Confidence:** {confidence_pct:.1f}%")
                            elif status == "debunked":
                                st.error(f"### ❌ DEBUNKED\n**Confidence:** {confidence_pct:.1f}%")
                            else:
                                st.warning(f"### ⚠️ INCONCLUSIVE\n**Confidence:** {confidence_pct:.1f}%")
                                
                            st.markdown(f"**Justification:** {data['justification']}")
                            
                            if data.get('sources'):
                                st.info("**Sources Analyzed:**\n" + "\n".join([f"- [{s}]({s})" for s in data['sources']]))
                        else:
                            st.error(f"Backend rejected the request: {response.text}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("🚨 Failed to connect to the backend. Ensure your Docker containers are running.")
    
    elif ingest_mode == "Batch Processing":
        with st.form("batch_form"):
            batch_text = st.text_area(
                "Enter multiple claims (one per line):", 
                placeholder="The moon landing was faked.\nNapoleon was extremely short.\nBats are entirely blind."
            )
            submitted_batch = st.form_submit_button("🔍 Scrutinize Batch")

        if submitted_batch:
            # Split the text area by newlines and remove empty lines
            claims_list = [c.strip() for c in batch_text.split('\n') if c.strip()]
            
            if not claims_list:
                st.error("I cannot investigate silence. Please enter at least one claim.")
            else:
                with st.spinner(f"Cross-referencing {len(claims_list)} claims sequentially. This may take a moment... 🕵️‍♂️"):
                    try:
                        response = requests.post(f"{API_URL}/verify/batch", json={"claims": claims_list})
                        
                        if response.status_code == 201:
                            results = response.json()
                            st.success(f"Successfully processed {len(results)} claims!")
                            
                            # Display each result in a neat expander
                            for data in results:
                                icon = "✅" if data['status'] == "verified" else "❌" if data['status'] == "debunked" else "⚠️"
                                with st.expander(f"{icon} {data['claim_text'][:60]}..."):
                                    st.write(f"**Verdict:** {data['status'].upper()} (Confidence: {(data['confidence'] or 0.0)*100:.1f}%)")
                                    st.write(f"**Justification:** {data['justification']}")
                                    if data.get('sources'):
                                        st.markdown("**Sources:**")
                                        for s in data['sources']:
                                            st.markdown(f"- [{s}]({s})")
                        else:
                            st.error(f"Backend rejected the batch request: {response.text}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("🚨 Failed to connect to the backend. Ensure your Docker containers are running.")

# TAB 2: Historical Log
with tab_log:
    st.subheader("Recent Investigations")
    st.markdown("A public ledger of our most recent fact-checks.")
    
    try:
        # Fetching more claims now since we have a dedicated page for it
        res = requests.get(f"{API_URL}/claims?limit=15")
        if res.status_code == 200:
            claims = res.json()
            if not claims:
                st.caption("No claims investigated yet.")
            
            for c in claims:
                icon = "✅" if c['status'] == "verified" else "❌" if c['status'] == "debunked" else "⚠️"
                # Using expanders for each claim keeps the log incredibly clean
                with st.expander(f"{icon} {c['claim_text'][:60]}..."):
                    st.write(f"**Full Claim:** {c['claim_text']}")
                    st.write(f"**Verdict:** {c['status'].upper()} (Confidence: {(c['confidence'] or 0.0)*100:.1f}%)")
                    st.write(f"**Justification:** {c['justification']}")
                    if c.get('sources'):
                        st.markdown("**Sources:**")
                        for s in c['sources']:
                            st.markdown(f"- [{s}]({s})")
        else:
            st.error("Failed to fetch claims from the database.")
    except Exception:
        st.warning("⚠️ Could not load history. Is the backend API running?")
