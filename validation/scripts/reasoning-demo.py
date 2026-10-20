#!/usr/bin/env python3
"""
SBMO validation — what the Pellet reasoner infers from the populated A-Box
(R30/R28/R34 of the defense revisions).

1. Realizes the 31 cases and counts the members of each defined class
   (SubscriptionSaaSModel, FreemiumSubscriptionModel, PlatformBusinessModel,
   NetworkedPlatformModel). Each set is compared with the set computed,
   independently of the reasoner, from survey-derived/cases_normalized.csv.
2. Checks the T-Box inference NetworkedPlatformModel SubClassOf
   PlatformBusinessModel.
3. Builds the "declared x inferred" table for Case02 (the Suassu case of
   Section 1.1 of the dissertation): asserted types, inferred named types, and
   the axioms of the first Pellet justification of each inference.
4. Open-world probes: Case02 is neither entailed to be a PlatformBusinessModel
   nor its complement; its declared standalone role is entailed not to be any of
   the other role types it is disjoint with.
5. Negative tests: each protege/case02-negative-test-*.ttl file imports the A-Box
   and adds one wrong assertion; the knowledge base must be inconsistent, and
   the Pellet justification of the inconsistency is reported.

Explanations come from Justify.java (Pellet's explanation API), compiled on the
fly into a temporary directory against the Pellet jars bundled with owlready2.

Outputs:
  - survey-derived/defined-class-counts.csv
  - survey-derived/case02-declared-inferred.csv
  - survey-derived/reasoning-demo.json (probes, negative tests, justifications)
  - LaTeX tables defined-class-counts.tex and case02-declared-inferred.tex in
    sbm-ontology-dissertation/assets/ontology_evaluation/tables/

Requirements (not stdlib): owlready2 (bundles Pellet 2.3.1) and rdflib, plus a
JDK (java and javac on PATH). Verified 2026-10-20 with owlready2 0.51, rdflib
7.6.0 and OpenJDK 27.

Usage:  python3 reasoning-demo.py
        python3 reasoning-demo.py --tbox OLD.rdf --abox OLD.ttl --negative-only
          (negative tests against another ontology version, no files written)
"""
import argparse, csv, json, os, shutil, subprocess, sys, tempfile
import rdflib
from rdflib import RDF, OWL, URIRef
import owlready2
from owlready2 import get_ontology, default_world, sync_reasoner_pellet, Thing, Not

HERE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.dirname(HERE)  # sbmo/validation
SBMO_ROOT = os.path.dirname(VAL)
DISSERTATION_ROOT = os.path.dirname(SBMO_ROOT)
TEX_DIR = os.path.join(DISSERTATION_ROOT, "sbm-ontology-dissertation", "assets",
                       "ontology_evaluation", "tables")
CASES = os.path.join(VAL, "survey-derived", "cases_normalized.csv")
NS = "https://rafaelc-rb.github.io/sbmo#"
EX = "https://rafaelc-rb.github.io/sbmo/abox#"
TBOX_IRI = "https://rafaelc-rb.github.io/sbmo"
MAX_JUSTIFICATIONS = 100  # search limit; reaching it is reported as a problem
NEGATIVE_TESTS = ["case02-negative-test-disjoint-roles.ttl",
                  "case02-negative-test-misused-value.ttl"]
DEFINED = ["SubscriptionSaaSModel", "FreemiumSubscriptionModel",
           "PlatformBusinessModel", "NetworkedPlatformModel"]
ROLE_TYPES = ["TwoSidedPlatform", "Marketplace", "OEMComponent", "PluginComplement"]

ap = argparse.ArgumentParser()
ap.add_argument("--tbox", default=os.path.join(SBMO_ROOT, "sbmo.rdf"))
ap.add_argument("--abox", default=os.path.join(VAL, "protege", "sbmo-validation-abox.ttl"))
ap.add_argument("--negative-only", action="store_true")
args = ap.parse_args()

short = lambda u: str(u).split("#")[-1]
problems = []


# --- helpers -------------------------------------------------------------------
def merged(*extra):
    """T-Box + A-Box (+ test files) as one RDF/XML ontology without imports."""
    g = rdflib.Graph()
    g.parse(args.tbox, format="xml")
    g.parse(args.abox, format="turtle")
    for f in extra:
        g.parse(f, format="turtle")
    for o in list(g.subjects(RDF.type, OWL.Ontology)):
        if str(o) != TBOX_IRI:
            g.remove((o, None, None))
    g.remove((None, OWL.imports, None))
    tmp = tempfile.NamedTemporaryFile(suffix=".rdf", delete=False)
    g.serialize(tmp.name, format="xml")
    return tmp.name


PELLET = os.path.join(os.path.dirname(owlready2.__file__), "pellet")
JARS = [os.path.join(PELLET, j) for j in sorted(os.listdir(PELLET)) if j.endswith(".jar")]
CLASSES = tempfile.mkdtemp(prefix="sbmo-justify-")
if not (shutil.which("java") and shutil.which("javac")):
    sys.exit("java and javac (a JDK) must be on PATH")
subprocess.run(["javac", "-nowarn", "-cp", ":".join(JARS), "-d", CLASSES,
                os.path.join(HERE, "Justify.java")], check=True, capture_output=True)
CP = ":".join([CLASSES] + JARS)


def justify(*a):
    """List of justifications; each is a list of (type, manchester, dl) axioms."""
    out = subprocess.run(["java", "-cp", CP, "Justify", *a, str(MAX_JUSTIFICATIONS)],
                         capture_output=True, text=True, check=True).stdout
    js = {}
    for line in out.splitlines():
        if line.startswith("J"):
            k, t, man, dl = line.split("\t")
            js.setdefault(k, []).append((t, man, dl))
    return list(js.values())


def consistent(path):
    out = subprocess.run(["java", "-cp", CP, "pellet.Pellet", "consistency", path],
                         capture_output=True, text=True).stdout
    return "Consistent: Yes" in out


def negative_tests():
    results = []
    for name in NEGATIVE_TESTS:
        path = merged(os.path.join(VAL, "protege", name))
        ok = consistent(path)
        js = [] if ok else justify("inconsistent", path)
        results.append({"test": name, "consistent": ok,
                        "justifications": [[m for _, m, _ in j] for j in js]})
        print(f"{name}: {'CONSISTENT' if ok else 'INCONSISTENT'}")
        for i, j in enumerate(js, 1):
            for _, m, _ in j:
                print(f"  J{i}  {m}")
    return results


if args.negative_only:
    negative_tests()
    sys.exit(0)

# --- 1. realization of the 31 cases --------------------------------------------
MERGED = merged()
onto = get_ontology("file://" + MERGED).load()
sb = default_world.get_namespace(NS)
with onto:  # complement probes for the open-world check (never written to disk)
    probes = {}
    for c in ["PlatformBusinessModel"] + ROLE_TYPES:
        P = type("Not" + c, (Thing,), {})
        P.equivalent_to = [Not(getattr(sb, c))]
        probes[c] = P
sync_reasoner_pellet(infer_property_values=False, debug=0)
PROBE_NAMES = {p.name for p in probes.values()}

rows = list(csv.DictReader(open(CASES, encoding="utf-8")))
has = lambda r, col, v: v in r[col].split(";")
platform = lambda r: has(r, "ecosystem", "TwoSidedPlatform") or has(r, "ecosystem", "Marketplace")
EXPECTED = {  # the definitions of sbmo.rdf, evaluated over the case table
    "SubscriptionSaaSModel": lambda r: has(r, "delivery", "MultiTenantSaaS") and has(r, "revenue", "SubscriptionRevenue"),
    "FreemiumSubscriptionModel": lambda r: has(r, "pricing", "FreemiumPricing") and has(r, "revenue", "SubscriptionRevenue"),
    "PlatformBusinessModel": platform,
    # build_abox.py links every network effect of a case to every ecosystem role of that case
    "NetworkedPlatformModel": lambda r: platform(r) and bool(r["network_effect"]),
}
n_cases = len(rows)
counts = []
print(f"Defined classes over {n_cases} cases:")
for c in DEFINED:
    got = sorted(short(i.iri) for i in getattr(sb, c).instances())
    exp = sorted(r["case_id"] for r in rows if EXPECTED[c](r))
    if got != exp:
        problems.append(f"{c}: reasoner {got} != expected {exp}")
    counts.append({"defined_class": c, "n_cases": len(got),
                   "pct": round(100 * len(got) / n_cases, 1), "cases": ";".join(got)})
    print(f"  {c}: {len(got)} ({100 * len(got) / n_cases:.1f}%) sets_equal={got == exp}")
member_of = {r["case_id"]: sum(r["case_id"] in x["cases"].split(";") for x in counts) for r in rows}
in_none = sorted(k for k, v in member_of.items() if v == 0)
print(f"  in no defined class: {len(in_none)} ({', '.join(in_none)})")

# --- 2. T-Box inference -----------------------------------------------------------
sub_ok = sb.PlatformBusinessModel in sb.NetworkedPlatformModel.ancestors()
sub_just = justify("subclass", MERGED, NS + "NetworkedPlatformModel", NS + "PlatformBusinessModel")
if not sub_ok:
    problems.append("NetworkedPlatformModel is not inferred to be a PlatformBusinessModel")
print(f"NetworkedPlatformModel SubClassOf PlatformBusinessModel: {sub_ok}")

# --- 3. Case02: declared x inferred ---------------------------------------------
abox = rdflib.Graph()
abox.parse(args.abox, format="turtle")
case = URIRef(EX + "Case02")
values = sorted({o for p, o in abox.predicate_objects(case)
                 if isinstance(o, URIRef) and p != RDF.type}, key=str)
mitigations = sorted({s for s in abox.subjects(URIRef(NS + "mitigates"), None)
                      if str(s).startswith(EX + "Case02_")}, key=str)
table = []
for ind in [case] + values + mitigations:
    declared = sorted(short(t) for t in abox.objects(ind, RDF.type))
    entity = default_world[str(ind)]
    named = {short(c.iri) for c in entity.INDIRECT_is_a
             if hasattr(c, "iri") and c.iri.startswith(NS)} - PROBE_NAMES
    for t in sorted(named - set(declared)):
        js = justify("instance", MERGED, str(ind), NS + t)
        if len(js) >= MAX_JUSTIFICATIONS:
            problems.append(f"{short(ind)} {t}: justification limit reached")
        table.append({"individual": short(ind), "declared": ";".join(declared), "inferred": t,
                      "n_justifications": len(js),
                      "justification_1": " ; ".join(m for _, m, _ in js[0]) if js else ""})
case02_inferred = [x["inferred"] for x in table if x["individual"] == "Case02"]
if set(case02_inferred) != {"FreemiumSubscriptionModel", "SubscriptionSaaSModel"}:
    problems.append(f"Case02 inferred classes: {case02_inferred}")
print("Case02 inferred:", case02_inferred)

# --- 4. open-world probes ---------------------------------------------------------
c02, role = default_world[EX + "Case02"], default_world[EX + "Case02_StandaloneProduct"]
probe = {
    "Case02 PlatformBusinessModel": c02 in sb.PlatformBusinessModel.instances(),
    "Case02 not PlatformBusinessModel": c02 in probes["PlatformBusinessModel"].instances(),
}
for c in ROLE_TYPES:
    probe[f"Case02_StandaloneProduct not {c}"] = role in probes[c].instances()
for k, v in probe.items():
    print(f"  {k}: {v}")
if probe["Case02 PlatformBusinessModel"] or probe["Case02 not PlatformBusinessModel"] \
        or not all(probe[f"Case02_StandaloneProduct not {c}"] for c in ROLE_TYPES):
    problems.append(f"open-world probes: {probe}")

# --- 5. negative tests -----------------------------------------------------------
neg = negative_tests()
problems += [f"{x['test']} is consistent" for x in neg if x["consistent"]]

# --- outputs ---------------------------------------------------------------------
def write_csv(path, rows_, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows_)


SD = os.path.join(VAL, "survey-derived")
write_csv(os.path.join(SD, "defined-class-counts.csv"), counts,
          ["defined_class", "n_cases", "pct", "cases"])
write_csv(os.path.join(SD, "case02-declared-inferred.csv"), table,
          ["individual", "declared", "inferred", "n_justifications", "justification_1"])
with open(os.path.join(SD, "reasoning-demo.json"), "w", encoding="utf-8") as f:
    json.dump({"n_cases": n_cases, "defined_classes": counts, "in_no_defined_class": in_none,
               "subsumption_NetworkedPlatformModel_PlatformBusinessModel":
                   {"inferred": sub_ok, "justification_1": [m for _, m, _ in sub_just[0]] if sub_just else []},
               "open_world_probes": probe, "negative_tests": neg,
               "max_justifications_searched": MAX_JUSTIFICATIONS}, f, indent=2)

GEN = "% Generated by sbmo/validation/scripts/reasoning-demo.py -- do not edit by hand."
tt = lambda s: r"\texttt{" + s + "}"
lines = [GEN, r"\begin{table}[!htb]", r"\renewcommand{\arraystretch}{1.3}",
         r"\caption[Cases classified by Pellet into each defined class]{Cases classified by "
         r"Pellet into each defined class (" + str(n_cases) + r" cases). No case was asserted as a "
         r"member of a defined class; the members coincide with the sets computed independently "
         r"from the questionnaire data.}",
         r"\label{tab:defined_class_counts}", r"\centering", r"\footnotesize",
         r"\begin{tabular}{l|c|c|>{\raggedright\arraybackslash}p{7.2cm}}", r"\bottomrule",
         r"\rowcolor{gray!50}",
         r"\textbf{Defined Class} & \textbf{Cases} & \textbf{\%} & \textbf{Members} \\", r"\hline"]
for x in counts:
    members = ", ".join(c.replace("Case", "") for c in x["cases"].split(";"))
    lines.append(rf"{tt(x['defined_class'])} & {x['n_cases']} & {x['pct']:.1f}\% & {members} \\")
lines += [r"\hline",
          rf"\multicolumn{{4}}{{l}}{{In no defined class: {len(in_none)} cases "
          rf"({', '.join(c.replace('Case', '') for c in in_none)}). Members are listed by case number.}} \\",
          r"\toprule", r"\end{tabular}", r"\end{table}", ""]
os.makedirs(TEX_DIR, exist_ok=True)
with open(os.path.join(TEX_DIR, "defined-class-counts.tex"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# compact declared x inferred table
by = {(x["individual"], x["inferred"]): x for x in table}
def premises(cls):
    """Asserted facts in the first justification of Case02's membership in cls."""
    j = by[("Case02", cls)]["justification_1"].split(" ; ")
    return [a for a in j if "EquivalentTo" not in a]
dims = [x for x in table if x["individual"] != "Case02" and x["individual"] not in
        {short(m) for m in mitigations}]
n_values = len(values)
value_just = sorted({x["n_justifications"] for x in dims})
neg_roles = [c for c in ROLE_TYPES if probe[f"Case02_StandaloneProduct not {c}"]]
fmt = lambda facts: r"; \newline ".join(tt(a.replace("_", r"\_")) for a in facts)
lines = [GEN, r"\begin{table}[!htb]", r"\renewcommand{\arraystretch}{1.3}",
         r"\caption[Declared and inferred knowledge about the Suassu case (Case02)]{Declared and "
         r"inferred knowledge about the Suassu case (\texttt{Case02}). \emph{Declared} lists the "
         r"A-Box assertions used by the first justification that Pellet returns; \emph{Inferred} "
         r"is what the reasoner derives from them and from the axioms in the last column.}",
         r"\label{tab:case02_declared_inferred}", r"\centering", r"\scriptsize",
         r"\begin{tabular}{>{\raggedright\arraybackslash}p{5.3cm}|>{\raggedright\arraybackslash}p{4.3cm}|>{\raggedright\arraybackslash}p{4.4cm}}",
         r"\bottomrule", r"\rowcolor{gray!50}",
         r"\textbf{Declared (A-Box)} & \textbf{Inferred by Pellet} & \textbf{Axioms Used (T-Box)} \\", r"\hline"]
for cls in ["SubscriptionSaaSModel", "FreemiumSubscriptionModel"]:
    lines.append(rf"{fmt(premises(cls))} & {tt('Case02')} is a {tt(cls)} & "
                 rf"definition of {tt(cls)} ($\equiv$); {by[('Case02', cls)]['n_justifications']} "
                 r"justifications in total, which differ only in how \texttt{Case02} is derived to be a "
                 r"\texttt{SoftwareBusinessModel} (assertion or domain of a property it uses) \\")
lines.append(rf"{tt(r'Case02 hasEcosystemRole Case02\_StandaloneProduct')}; {tt(r'Case02\_StandaloneProduct Type StandaloneProduct')} & "
             rf"{tt(r'Case02\_StandaloneProduct')} is not a " + ", ".join(tt(c) for c in neg_roles[:-1]) + ", or " + tt(neg_roles[-1]) +
             r" & disjointness of \texttt{StandaloneProduct} with each of these role types \\")
lines.append(rf"{tt(r'Case02 hasEcosystemRole Case02\_StandaloneProduct')} & neither "
             rf"{tt('PlatformBusinessModel')} nor its complement & open-world assumption: no "
             r"axiom states that the asserted role is the only one \\")
lines.append(rf"{n_values} value individuals, each typed with a leaf class (\textit{{e.g.}}, "
             rf"{tt(r'Case02\_UserSeat Type UserSeat')}) & each is a member of its dimensional class "
             rf"(\textit{{e.g.}}, {tt('PricingBaseUnit')}) & subclass axiom and range of the linking "
             rf"property ({'--'.join(str(v) for v in value_just)} justifications each) \\")
lines.append(rf"{len(mitigations)} mitigation individuals linked by {tt('mitigates')} & each is a "
             rf"{tt('MitigationStrategy')} & subclass axiom and domain of {tt('mitigates')} \\")
lines += [r"\toprule", r"\end{tabular}", r"\end{table}", ""]
with open(os.path.join(TEX_DIR, "case02-declared-inferred.tex"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("ALL OK" if not problems else "MISMATCH:\n  " + "\n  ".join(problems))
sys.exit(0 if not problems else 1)
