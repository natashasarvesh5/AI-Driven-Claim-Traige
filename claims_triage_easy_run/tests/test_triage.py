import unittest
from app.triage_engine import triage_claim
class TestTriage(unittest.TestCase):
 def test_simple_fast_track(self):
  r=triage_claim({"claim_id":"T1","claim_type":"Auto","description":"minor scratch photos attached","estimated_amount":500,"location":"Pune","documents_count":2})
  self.assertEqual(r["route"],"Fast Track Queue")
 def test_urgent_complex(self):
  r=triage_claim({"claim_id":"T2","claim_type":"Auto","description":"multiple vehicles severe injury hospital liability disputed","estimated_amount":100000,"location":"Mumbai","injuries":2,"parties":4,"hours_since_loss":2,"documents_count":3})
  self.assertIn(r["priority"],["High","Critical"]); self.assertEqual(r["route"],"Senior / Complex Claims Team")
if __name__=="__main__": unittest.main()
