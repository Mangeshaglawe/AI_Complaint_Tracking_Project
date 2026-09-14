import json
from pathlib import Path

import pandas as pd
import streamlit as st

from .main import run_batch, DATA_DIR, OUT_DIR


st.set_page_config(page_title="Complaint Pipeline Dashboard", layout="wide")


if "pipeline_state" not in st.session_state:
    st.session_state.pipeline_state = {
        "status": "idle",
        "total_documents": 0,
        "processed_documents": 0,
        "results": [],
        "errors": [],
        "files": [],
        "report_path": "",
        "success_count": 0,
        "error_count": 0,
    }


def update_state(payload):
    state = st.session_state.pipeline_state
    state["status"] = payload.get("status", state["status"])
    if payload.get("type") == "start":
        state["total_documents"] = payload.get("total", 0)
        state["processed_documents"] = 0
    elif payload.get("type") == "progress":
        state["processed_documents"] = payload.get("processed", state["processed_documents"])
        state["status"] = payload.get("status", state["status"])
    elif payload.get("type") == "complete":
        state["success_count"] = payload.get("success_count", 0)
        state["error_count"] = payload.get("error_count", 0)
    elif payload.get("type") == "error":
        state["errors"].append(payload.get("message"))


st.title("Complaint Processing Dashboard")

left, right = st.columns(2)
with left:
    st.subheader("Pipeline control")
    max_workers = st.slider("Worker threads", min_value=1, max_value=8, value=4)
    run_button = st.button("Run batch pipeline")

with right:
    st.subheader("Live status")
    status = st.session_state.pipeline_state["status"]
    st.metric("Status", status.upper())
    st.metric("Processed", f"{st.session_state.pipeline_state['processed_documents']} / {st.session_state.pipeline_state['total_documents']}")

if run_button:
    state = st.session_state.pipeline_state
    state["status"] = "running"
    state["results"] = []
    state["errors"] = []
    state["files"] = [p.name for p in DATA_DIR.iterdir() if p.is_file()]
    state["total_documents"] = len(state["files"])
    state["processed_documents"] = 0
    progress_bar = st.progress(0)
        
    def cb(payload):
        update_state(payload)
        if payload.get("type") == "progress":
            total = max(payload.get("total", 1), 1)
            processed = payload.get("processed", 0)
            progress_bar.progress(processed / total)
        elif payload.get("type") == "complete":
            progress_bar.progress(1.0)

    try:
        results = run_batch(max_workers=max_workers, progress_callback=cb, state=state)
        st.success(f"Processing complete. {len(results)} files evaluated.")
    except Exception as exc:
        st.error(f"Pipeline error: {exc}")


st.subheader("Analytics")
state = st.session_state.pipeline_state
summary_df = pd.DataFrame(state["results"])
if not summary_df.empty:
    if "error" in summary_df.columns:
        summary_df["has_error"] = summary_df["error"].notna()
    st.dataframe(summary_df, use_container_width=True)

    counts = summary_df["has_error"].value_counts().to_dict() if "has_error" in summary_df.columns else {"False": len(summary_df)}
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Successful records", counts.get(False, 0))
    with c2:
        st.metric("Errored records", counts.get(True, 0))
else:
    st.info("No results yet. Run the batch pipeline to populate the dashboard.")

st.subheader("Recent errors")
if state["errors"]:
    for err in state["errors"][-10:]:
        st.write(err)
else:
    st.write("No errors recorded.")

st.subheader("Output paths")
if OUT_DIR.exists():
    for item in sorted(OUT_DIR.rglob("*")):
        if item.is_file():
            st.code(str(item.relative_to(Path.cwd())))
