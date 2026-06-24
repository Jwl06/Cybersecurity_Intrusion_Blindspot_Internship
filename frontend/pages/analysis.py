"""Analysis — network traffic input and XGBoost threat prediction dashboard."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import requests
import streamlit as st

from utils.api import api_available, predict_traffic
from utils.nav import render_sidebar
from utils.theme import (
    analysis_history_table,
    attack_type_panel,
    inject_theme,
    prediction_panel,
    risk_gauge,
    section_divider,
    soc_status_bar,
    threat_statistics_row,
)

st.set_page_config(
    page_title="Analysis | Cybersecurity Intrusion Blindspot",
    page_icon=None,
    layout="wide",
)

inject_theme()
render_sidebar()

PROTOCOLS = ["TCP", "UDP", "ICMP"]

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; sqlmap/1.7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "curl/7.81.0",
    "curl/8.4.0",
    "python-requests/2.28",
    "python-requests/2.31.0",
    "python-urllib/3.9",
    "sqlmap/1.8",
    "zgrab/0.x",
]

ATTACK_SCENARIOS: dict[str, dict[str, Any]] = {
    "HTTPS Browsing (Normal)": {
        "protocol": "TCP",
        "src_port": 52104,
        "dst_port": 443,
        "bytes_sent": 1200.0,
        "bytes_received": 4500.0,
        "user_agent": USER_AGENTS[1],
        "is_internal_traffic": False,
    },
    "SSH Brute Force": {
        "protocol": "TCP",
        "src_port": 33412,
        "dst_port": 22,
        "bytes_sent": 890.0,
        "bytes_received": 420.0,
        "user_agent": USER_AGENTS[6],
        "is_internal_traffic": False,
    },
    "SQL Injection Probe": {
        "protocol": "TCP",
        "src_port": 44890,
        "dst_port": 80,
        "bytes_sent": 2400.0,
        "bytes_received": 1800.0,
        "user_agent": USER_AGENTS[11],
        "is_internal_traffic": False,
    },
    "Port Scan (zgrab)": {
        "protocol": "TCP",
        "src_port": 51200,
        "dst_port": 8080,
        "bytes_sent": 320.0,
        "bytes_received": 180.0,
        "user_agent": USER_AGENTS[12],
        "is_internal_traffic": False,
    },
    "ICMP Flood": {
        "protocol": "ICMP",
        "src_port": 0,
        "dst_port": 0,
        "bytes_sent": 120_000.0,
        "bytes_received": 800.0,
        "user_agent": USER_AGENTS[6],
        "is_internal_traffic": False,
    },
}

def _short_user_agent(ua: str) -> str:
    if len(ua) <= 48:
        return ua
    return ua[:45] + "..."


def _history_entry(
    *,
    time: str,
    payload: dict[str, Any],
    prediction: str,
    confidence: float,
    risk: str,
    risk_variant: str,
    attack_type: str,
    score: float,
) -> dict[str, Any]:
    """Build a normalized history row with all flow and classification fields."""
    return {
        "time": time,
        "protocol": payload["protocol"],
        "src_port": int(payload["src_port"]),
        "dst_port": int(payload["dst_port"]),
        "ports": f"{payload['src_port']}→{payload['dst_port']}",
        "bytes_sent": float(payload["bytes_sent"]),
        "bytes_received": float(payload["bytes_received"]),
        "volume": f"{int(payload['bytes_sent']):,} / {int(payload['bytes_received']):,}",
        "user_agent": payload["user_agent"],
        "user_agent_short": _short_user_agent(payload["user_agent"]),
        "internal": bool(payload["is_internal_traffic"]),
        "prediction": prediction,
        "confidence": confidence,
        "risk": risk,
        "risk_variant": risk_variant,
        "attack_type": attack_type,
        "score": score,
    }


SEED_HISTORY: list[dict] = [
    _history_entry(
        time="09:14:22",
        payload=ATTACK_SCENARIOS["HTTPS Browsing (Normal)"],
        prediction="Normal",
        confidence=0.94,
        risk="Minimal",
        risk_variant="minimal",
        attack_type="Benign Traffic",
        score=0.06,
    ),
    _history_entry(
        time="10:38:51",
        payload=ATTACK_SCENARIOS["SSH Brute Force"],
        prediction="Attack",
        confidence=0.82,
        risk="High",
        risk_variant="high",
        attack_type="Brute Force",
        score=0.78,
    ),
    _history_entry(
        time="11:02:17",
        payload=ATTACK_SCENARIOS["SQL Injection Probe"],
        prediction="Attack",
        confidence=0.91,
        risk="Critical",
        risk_variant="critical",
        attack_type="SQL Injection",
        score=0.91,
    ),
    _history_entry(
        time="11:47:09",
        payload=ATTACK_SCENARIOS["Port Scan (zgrab)"],
        prediction="Attack",
        confidence=0.76,
        risk="High",
        risk_variant="high",
        attack_type="Port / Service Scan",
        score=0.74,
    ),
    _history_entry(
        time="12:18:44",
        payload={
            **ATTACK_SCENARIOS["HTTPS Browsing (Normal)"],
            "src_port": 49821,
            "dst_port": 443,
            "user_agent": USER_AGENTS[5],
        },
        prediction="Normal",
        confidence=0.89,
        risk="Low",
        risk_variant="low",
        attack_type="Benign Traffic",
        score=0.11,
    ),
    _history_entry(
        time="12:45:03",
        payload=ATTACK_SCENARIOS["ICMP Flood"],
        prediction="Attack",
        confidence=0.88,
        risk="Critical",
        risk_variant="critical",
        attack_type="Flooding / DoS",
        score=0.87,
    ),
    _history_entry(
        time="13:22:31",
        payload={
            "protocol": "TCP",
            "src_port": 60214,
            "dst_port": 3389,
            "bytes_sent": 2100.0,
            "bytes_received": 980.0,
            "user_agent": USER_AGENTS[8],
            "is_internal_traffic": True,
        },
        prediction="Attack",
        confidence=0.71,
        risk="Medium",
        risk_variant="medium",
        attack_type="Automated Probe",
        score=0.58,
    ),
    _history_entry(
        time="14:05:18",
        payload={
            "protocol": "UDP",
            "src_port": 53112,
            "dst_port": 53,
            "bytes_sent": 512.0,
            "bytes_received": 1024.0,
            "user_agent": USER_AGENTS[0],
            "is_internal_traffic": False,
        },
        prediction="Normal",
        confidence=0.92,
        risk="Minimal",
        risk_variant="minimal",
        attack_type="Benign Traffic",
        score=0.08,
    ),
]


def _seed_threat_stats() -> dict[str, float | int]:
    attacks = sum(1 for row in SEED_HISTORY if row["prediction"] == "Attack")
    normal = len(SEED_HISTORY) - attacks
    score_sum = sum(row["score"] for row in SEED_HISTORY)
    return {
        "total": len(SEED_HISTORY),
        "attacks": attacks,
        "normal": normal,
        "score_sum": score_sum,
    }


def _init_session_state() -> None:
    if "analysis_history_version" not in st.session_state:
        st.session_state.analysis_history_version = 2
        st.session_state.analysis_history = list(SEED_HISTORY)
        st.session_state.threat_stats = _seed_threat_stats()
    elif st.session_state.analysis_history_version < 2:
        st.session_state.analysis_history_version = 2
        st.session_state.analysis_history = list(SEED_HISTORY)
        st.session_state.threat_stats = _seed_threat_stats()
    elif "analysis_history" not in st.session_state:
        st.session_state.analysis_history = list(SEED_HISTORY)
    if "threat_stats" not in st.session_state:
        st.session_state.threat_stats = _seed_threat_stats()
    if "last_analysis" not in st.session_state:
        st.session_state.last_analysis = None
    if "analysis_error" not in st.session_state:
        st.session_state.analysis_error = None
    if "traffic_defaults" not in st.session_state:
        st.session_state.traffic_defaults = ATTACK_SCENARIOS["HTTPS Browsing (Normal)"]


def _risk_level(prediction: str, attack_probability: float) -> tuple[str, str]:
    """Return risk label and CSS variant from prediction output."""
    if prediction == "Attack":
        if attack_probability >= 0.85:
            return "Critical", "critical"
        if attack_probability >= 0.65:
            return "High", "high"
        return "Medium", "medium"
    if attack_probability >= 0.35:
        return "Medium", "medium"
    if attack_probability >= 0.15:
        return "Low", "low"
    return "Minimal", "minimal"


def _recommended_action(prediction: str, risk: str) -> str:
    """Return operational guidance based on classification."""
    if prediction == "Attack":
        if risk in {"Critical", "High"}:
            return "Block session immediately and escalate to the security operations center."
        return "Quarantine flow for manual review and enable enhanced packet logging."
    if risk == "Medium":
        return "Allow with monitoring — flag session for analyst review within 24 hours."
    return "Allow traffic — continue standard monitoring."


def _infer_attack_type(payload: dict, prediction: str) -> tuple[str, str, list[str]]:
    """Heuristically classify attack type from flow features."""
    ua = payload["user_agent"].lower()
    dst_port = int(payload["dst_port"])
    src_port = int(payload["src_port"])
    protocol = payload["protocol"]
    bytes_sent = float(payload["bytes_sent"])
    bytes_received = float(payload["bytes_received"])
    internal = payload["is_internal_traffic"]

    if prediction == "Normal":
        return (
            "Benign Traffic",
            "Flow characteristics align with legitimate application or browsing behavior.",
            ["Expected port usage", "Standard user-agent profile"],
        )

    if "sqlmap" in ua:
        return (
            "SQL Injection",
            "Automated SQL injection tooling detected in the user-agent string.",
            ["SQLmap signature", f"dst:{dst_port}", protocol],
        )

    if "zgrab" in ua:
        return (
            "Port / Service Scan",
            "Network reconnaissance scanner probing exposed services.",
            ["zgrab scanner", f"dst:{dst_port}", protocol],
        )

    if any(tool in ua for tool in ("curl/", "python-requests", "python-urllib")):
        return (
            "Automated Probe",
            "Scripted HTTP client activity inconsistent with typical browser sessions.",
            ["Scripted client", f"bytes:{int(bytes_sent)}", protocol],
        )

    if dst_port in {22, 21, 3389, 23} and bytes_sent < 5000:
        return (
            "Brute Force",
            "Low-volume traffic targeting administrative or authentication services.",
            [f"auth-port:{dst_port}", f"src:{src_port}", protocol],
        )

    if protocol == "ICMP" or bytes_sent > 50_000 or bytes_received > 50_000:
        return (
            "Flooding / DoS",
            "Elevated packet volume or ICMP usage suggesting denial-of-service activity.",
            [protocol, f"sent:{int(bytes_sent)}", f"recv:{int(bytes_received)}"],
        )

    if "googlebot" in ua and not internal:
        return (
            "Spoofed Reconnaissance",
            "Suspicious crawler impersonation from an external source.",
            ["UA spoofing", "External origin", protocol],
        )

    return (
        "Suspicious Network Activity",
        "Anomalous flow patterns flagged by the classifier without a definitive subtype.",
        [protocol, f"{src_port}→{dst_port}", "XGBoost alert"],
    )


def _record_analysis(
    payload: dict,
    prediction: str,
    confidence: float,
    attack_probability: float,
    risk: str,
    risk_variant: str,
    attack_type: str,
) -> None:
    """Append a result to session history and update aggregate statistics."""
    entry = _history_entry(
        time=datetime.now().strftime("%H:%M:%S"),
        payload=payload,
        prediction=prediction,
        confidence=confidence,
        risk=risk,
        risk_variant=risk_variant,
        attack_type=attack_type,
        score=attack_probability,
    )
    history: list[dict] = st.session_state.analysis_history
    history.insert(0, entry)
    st.session_state.analysis_history = history[:12]

    stats = st.session_state.threat_stats
    stats["total"] += 1
    if prediction == "Attack":
        stats["attacks"] += 1
    else:
        stats["normal"] += 1
    stats["score_sum"] += attack_probability


def _build_analysis_result(payload: dict, api_result: dict) -> dict[str, Any]:
    """Derive display fields from API output and flow features."""
    prediction = api_result["prediction"]
    confidence = api_result["confidence"]
    attack_probability = api_result["attack_probability"]
    risk, risk_variant = _risk_level(prediction, attack_probability)
    attack_type, attack_desc, indicators = _infer_attack_type(payload, prediction)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "attack_probability": attack_probability,
        "risk": risk,
        "risk_variant": risk_variant,
        "action": _recommended_action(prediction, risk),
        "variant": "attack" if prediction == "Attack" else "normal",
        "attack_type": attack_type,
        "attack_desc": attack_desc,
        "indicators": indicators,
        "payload": payload,
    }


def _run_prediction(payload: dict) -> None:
    """Call the inference API and persist results in session state."""
    st.session_state.analysis_error = None

    if not api_available():
        st.session_state.last_analysis = None
        st.session_state.analysis_error = (
            "Inference API is offline. Start the backend server to run predictions."
        )
        return

    try:
        api_result = predict_traffic(payload)
        result = _build_analysis_result(payload, api_result)
        _record_analysis(
            payload,
            result["prediction"],
            result["confidence"],
            result["attack_probability"],
            result["risk"],
            result["risk_variant"],
            result["attack_type"],
        )
        st.session_state.last_analysis = result
    except requests.HTTPError as exc:
        detail = exc.response.text if exc.response is not None else str(exc)
        st.session_state.last_analysis = None
        st.session_state.analysis_error = f"Prediction failed: {detail}"
    except requests.RequestException as exc:
        st.session_state.last_analysis = None
        st.session_state.analysis_error = f"Could not reach inference API: {exc}"


def _render_analysis_result(result: dict[str, Any]) -> None:
    """Render prediction panel, risk gauge, and attack type analysis."""
    prediction_panel(
        prediction=result["prediction"],
        confidence=result["confidence"],
        risk=result["risk"],
        risk_variant=result["risk_variant"],
        action=result["action"],
        variant=result["variant"],
    )

    gauge_col, attack_col = st.columns(2, gap="small")
    with gauge_col:
        risk_gauge(result["attack_probability"], result["risk"], result["risk_variant"])
    with attack_col:
        attack_type_panel(
            result["attack_type"],
            result["attack_desc"],
            result["indicators"],
            is_threat=result["prediction"] == "Attack",
        )


def _clear_session_history() -> None:
    """Reset history and statistics to empty session state."""
    st.session_state.analysis_history = []
    st.session_state.threat_stats = {
        "total": 0,
        "attacks": 0,
        "normal": 0,
        "score_sum": 0.0,
    }


_init_session_state()
defaults = st.session_state.traffic_defaults

st.markdown('<p class="cyber-header">Threat Classification</p>', unsafe_allow_html=True)
st.markdown('<p class="cyber-title">Network Traffic Analysis</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="cyber-subtitle">Run XGBoost classification on live flow parameters and monitor '
    "threat statistics, risk scoring, and session analysis history.</p>",
    unsafe_allow_html=True,
)

form_col, result_col = st.columns([5, 4], gap="large")

with form_col:
    with st.container(border=True):
        section_divider("Network Traffic Input")

        scenario = st.selectbox(
            "Load Attack Scenario",
            list(ATTACK_SCENARIOS),
            help="Pre-fill the form with a representative traffic profile.",
        )
        if st.button("Apply Scenario", use_container_width=True):
            st.session_state.traffic_defaults = dict(ATTACK_SCENARIOS[scenario])
            st.rerun()

        defaults = st.session_state.traffic_defaults

        with st.form("traffic_form", clear_on_submit=False):
            endpoint_cols = st.columns(3)
            with endpoint_cols[0]:
                protocol = st.selectbox("Protocol", PROTOCOLS, index=PROTOCOLS.index(defaults["protocol"]))
            with endpoint_cols[1]:
                src_port = st.number_input(
                    "Source Port",
                    min_value=0,
                    max_value=65535,
                    value=int(defaults["src_port"]),
                    step=1,
                )
            with endpoint_cols[2]:
                dst_port = st.number_input(
                    "Destination Port",
                    min_value=0,
                    max_value=65535,
                    value=int(defaults["dst_port"]),
                    step=1,
                )

            volume_cols = st.columns(2)
            with volume_cols[0]:
                bytes_sent = st.number_input(
                    "Bytes Sent",
                    min_value=0.0,
                    value=float(defaults["bytes_sent"]),
                    step=1.0,
                )
            with volume_cols[1]:
                bytes_received = st.number_input(
                    "Bytes Received",
                    min_value=0.0,
                    value=float(defaults["bytes_received"]),
                    step=1.0,
                )

            ua_index = USER_AGENTS.index(defaults["user_agent"]) if defaults["user_agent"] in USER_AGENTS else 0
            user_agent = st.selectbox(
                "User Agent",
                USER_AGENTS,
                index=ua_index,
                format_func=_short_user_agent,
            )

            is_internal_traffic = st.toggle("Internal Traffic", value=bool(defaults["is_internal_traffic"]))

            predict_clicked = st.form_submit_button(
                "Run XGBoost Prediction",
                type="primary",
                use_container_width=True,
            )

with result_col:
    with st.container(border=True):
        section_divider("XGBoost Prediction")

        if predict_clicked:
            payload = {
                "protocol": protocol,
                "src_port": int(src_port),
                "dst_port": int(dst_port),
                "bytes_sent": float(bytes_sent),
                "bytes_received": float(bytes_received),
                "user_agent": user_agent,
                "is_internal_traffic": is_internal_traffic,
            }
            _run_prediction(payload)

        if st.session_state.analysis_error:
            st.error(st.session_state.analysis_error)

        if st.session_state.last_analysis:
            _render_analysis_result(st.session_state.last_analysis)
        elif not st.session_state.analysis_error:
            st.markdown(
                """
                <div class="prediction-placeholder">
                    <p class="prediction-placeholder-title">Awaiting Input</p>
                    <p class="prediction-placeholder-text">
                        Configure network flow parameters and run the XGBoost model to view
                        classification results, risk gauge, attack type analysis, and
                        recommended actions.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

stats = st.session_state.threat_stats
api_status = "ONLINE" if api_available() else "OFFLINE"
soc_status_bar(
    console="SOC-ANALYSIS",
    posture="ACTIVE SCAN",
    threats=f"{stats['attacks']} LOGGED",
    model=api_status,
)

st.markdown("<div style='height:0.85rem'></div>", unsafe_allow_html=True)

with st.container(border=True):
    section_divider("Threat Statistics")
    avg_score = stats["score_sum"] / stats["total"] if stats["total"] else 0.0
    threat_statistics_row(
        total_scans=stats["total"],
        threats_detected=stats["attacks"],
        clean_traffic=stats["normal"],
        avg_threat_score=avg_score,
    )

with st.container(border=True):
    history_title_col, history_action_col = st.columns([6, 1])
    with history_title_col:
        section_divider("Recent Analysis History")
    with history_action_col:
        st.markdown("<div style='height:0.15rem'></div>", unsafe_allow_html=True)
        if st.button("Clear", help="Reset session history and statistics", use_container_width=True):
            _clear_session_history()
            st.session_state.last_analysis = None
            st.session_state.analysis_error = None
            st.rerun()

    analysis_history_table(st.session_state.analysis_history)
