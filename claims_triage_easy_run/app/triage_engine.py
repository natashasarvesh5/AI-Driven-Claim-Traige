import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

URGENT_TERMS = {"hospital":18,"icu":25,"fatal":30,"death":30,"severe injury":22,"fire":18,"flood":14,"uninhabitable":18,"stolen":12,"theft":10,"emergency":20}
COMPLEX_TERMS = {"multiple vehicles":18,"third party":10,"lawyer":16,"litigation":18,"liability disputed":20,"commercial":10,"structural":14,"injury":12,"international":12,"police report":5}
FRAUD_TERMS = {"cash only":14,"no witnesses":8,"recent policy":12,"inconsistent":16,"duplicate":24,"staged":28,"unverified":10}

@dataclass
class TriageResult:
    claim_id: str
    urgency_score: int
    complexity_score: int
    risk_score: int
    priority: str
    route: str
    confidence: float
    reasons: list
    missing_fields: list
    processed_at: str
    engine_version: str = "prototype-rules-1.0"

def _clamp(v): return max(0, min(100, int(round(v))))
def _hits(text, mapping): return [(term, pts) for term, pts in mapping.items() if term in text]

def triage_claim(claim):
    text = " ".join(str(claim.get(k, "")) for k in ("claim_type","description","location")).lower()
    amount = float(claim.get("estimated_amount") or 0)
    injuries = int(claim.get("injuries") or 0)
    parties = int(claim.get("parties") or 1)
    hours = float(claim.get("hours_since_loss") or 24)
    docs = int(claim.get("documents_count") or 0)
    prior = int(claim.get("prior_claims") or 0)

    u_hits, c_hits, f_hits = _hits(text, URGENT_TERMS), _hits(text, COMPLEX_TERMS), _hits(text, FRAUD_TERMS)
    urgency = 10 + sum(p for _,p in u_hits) + min(injuries*15,35) + (18 if hours <= 6 else 8 if hours <= 24 else 0)
    complexity = 8 + sum(p for _,p in c_hits) + min(max(parties-1,0)*8,24) + (22 if amount>=100000 else 12 if amount>=25000 else 4 if amount>=5000 else 0) + (8 if docs==0 else 0)
    risk = 5 + sum(p for _,p in f_hits) + min(prior*7,28) + (10 if amount>=75000 else 0) + (8 if docs==0 else 0)
    urgency, complexity, risk = map(_clamp, (urgency,complexity,risk))

    required = ["claim_id","claim_type","description","estimated_amount","location"]
    missing = [f for f in required if claim.get(f) in (None, "")]
    reasons = []
    reasons += [f"Urgency signal: '{t}' (+{p})" for t,p in u_hits]
    reasons += [f"Complexity signal: '{t}' (+{p})" for t,p in c_hits]
    reasons += [f"Risk signal: '{t}' (+{p})" for t,p in f_hits]
    if injuries: reasons.append(f"Reported injuries: {injuries}")
    if parties > 1: reasons.append(f"Multiple parties: {parties}")
    if amount >= 25000: reasons.append(f"High estimated amount: {amount:,.0f}")
    if missing: reasons.append("Missing required fields: " + ", ".join(missing))

    if risk >= 45:
        route = "Special Investigation Review"
    elif complexity >= 65 or injuries >= 2:
        route = "Senior / Complex Claims Team"
    elif urgency >= 60:
        route = "Urgent Response Queue"
    elif complexity <= 35 and risk < 30 and not missing:
        route = "Fast Track Queue"
    else:
        route = "General Adjuster Queue"

    overall = max(urgency, int(complexity*.85), int(risk*.9))
    priority = "Critical" if overall>=75 else "High" if overall>=55 else "Medium" if overall>=35 else "Low"
    confidence = max(.55, min(.97, .92 - len(missing)*.08 - (0.07 if len(reasons)<2 else 0)))
    return asdict(TriageResult(
        claim_id=str(claim.get("claim_id") or "UNASSIGNED"), urgency_score=urgency,
        complexity_score=complexity, risk_score=risk, priority=priority, route=route,
        confidence=round(confidence,2), reasons=reasons or ["Standard claim profile; no strong exception signals"],
        missing_fields=missing, processed_at=datetime.now(timezone.utc).isoformat()))
