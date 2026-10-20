#!/usr/bin/env python3
"""
SBMO validation — re-run the seven competency-question DL queries with Pellet
and compare the returned individual SETS (not only their counts) with the sets
expected from the questionnaire data.

The DL Query expressions are read verbatim from protege/dl_queries.md. Each is
declared as a defined class over the T-Box (../sbmo.rdf) plus the anonymized
A-Box (protege/sbmo-validation-abox.ttl); Pellet then realizes the individuals.
The expected sets are computed, independently of the reasoner, from
survey-derived/cases_normalized.csv (CQ6: the mitigation-strategy individuals of
cases that also selected a challenge, as asserted by build_abox.py).

Requirements (not stdlib): owlready2 (bundles Pellet 2.3.1) and rdflib, plus a
Java runtime that can load the bundled jars. Verified 2026-10-19 with
owlready2 0.51, rdflib 7.6.0 and OpenJDK 27: all seven sets equal.

Usage:  python3 check_cq_result_sets.py
"""
import csv, os, re, sys, tempfile
import rdflib
from owlready2 import (get_ontology, default_world, sync_reasoner_pellet, Thing,
                       Or, And, Not)

VAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # sbmo/validation
TBOX = os.path.join(os.path.dirname(VAL), "sbmo.rdf")
ABOX = os.path.join(VAL, "protege", "sbmo-validation-abox.ttl")

g = rdflib.Graph()
g.parse(TBOX, format="xml")
g.parse(ABOX, format="turtle")
g.remove((None, rdflib.OWL.imports, None))
tmp = tempfile.NamedTemporaryFile(suffix=".nt", delete=False)
g.serialize(tmp.name, format="nt")
onto = get_ontology("file://" + tmp.name).load()
NS = "https://rafaelc-rb.github.io/sbmo#"
EX = "https://rafaelc-rb.github.io/sbmo/abox#"
sb = default_world.get_namespace(NS)

# --- tiny Manchester parser for: and / or / some / parentheses / names -------
def tokenize(s):
    return re.findall(r"\(|\)|[\w:]+", s)

def parse(tokens):
    def expr(i):
        left, i = term(i)
        items, op = [left], None
        while i < len(tokens) and tokens[i] in ("and", "or"):
            op = tokens[i]
            nxt, i = term(i + 1)
            items.append(nxt)
        if op is None:
            return left, i
        return (And(items) if op == "and" else Or(items)), i
    def term(i):
        if tokens[i] == "(":
            e, i = expr(i + 1)
            assert tokens[i] == ")"
            return e, i + 1
        name = tokens[i].split(":")[1]
        if i + 1 < len(tokens) and tokens[i + 1] == "some":
            filler, j = term(i + 2)
            return getattr(sb, name).some(filler), j
        ent = getattr(sb, name)
        assert ent is not None, name
        return ent, i + 1
    e, i = expr(0)
    assert i == len(tokens)
    return e

queries = {}
for line in open(os.path.join(VAL, "protege", "dl_queries.md"), encoding="utf-8"):
    m = re.match(r"\| (CQ\d) \| `([^`]+)` \| (\d+) \|", line)
    if m:
        queries[m.group(1)] = (m.group(2), int(m.group(3)))
assert len(queries) == 7

with onto:
    qcls = {}
    for cq, (expr, _) in queries.items():
        C = type("Q_" + cq, (Thing,), {})
        C.equivalent_to = [parse(tokenize(expr))]
        qcls[cq] = C

sync_reasoner_pellet(infer_property_values=False, debug=0)

# --- expected sets from the anonymized case table ---------------------------
rows = list(csv.DictReader(open(os.path.join(VAL, "survey-derived", "cases_normalized.csv"))))
has = lambda r, *ks: all(r[k] for k in ks)
exp = {
    "CQ1": {r["case_id"] for r in rows if has(r, "revenue", "delivery")},
    "CQ2": {r["case_id"] for r in rows if has(r, "pricing", "revenue")},
    "CQ3": {r["case_id"] for r in rows if has(r, "customer", "channel")},
    "CQ4": {r["case_id"] for r in rows if has(r, "ecosystem", "network_effect")},
    "CQ5": {r["case_id"] for r in rows if has(r, "success", "challenge")},
    "CQ6": {f"{r['case_id']}_{m}" for r in rows if r["challenge"]
            for m in r["mitigation"].split(";") if m},
    "CQ7": {r["case_id"] for r in rows if has(r, "delivery", "revenue", "pricing", "ecosystem")},
}
ok = True
for cq, C in qcls.items():
    got = {i.iri.split("#")[1] for i in C.instances()}
    same = got == exp[cq]
    ok &= same and len(got) == queries[cq][1]
    print(f"{cq}: returned={len(got)} expected={len(exp[cq])} documented={queries[cq][1]} "
          f"sets_equal={same}" + ("" if same else f" diff={sorted(got ^ exp[cq])}"))
print("ALL OK" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
