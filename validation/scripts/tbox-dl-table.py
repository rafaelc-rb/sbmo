#!/usr/bin/env python3
"""
SBMO validation — the T-Box of sbmo.rdf in description logic notation
(R27 of the defense revisions).

Reads the canonical T-Box and writes the dissertation table that summarizes
its logical axioms by type, in the DL notation of Section 6.4.3: subsumption
between named classes, domains and ranges of the object and data properties,
minimum cardinality restrictions, disjointness (between the configuration
dimensions and within them), and the defined classes. Axioms already listed
elsewhere in the dissertation are summarized by a schema and a reference
(subclasses: tab:subclasses; object property domains and ranges:
tab:object_properties; disjointness within dimensions and class definitions:
Section 6.4.3). The minimum cardinality restrictions and the disjointness
between dimensions are written out in full.

The script also checks that every logical axiom of the file falls in one of
these groups and that the counts add up to the 150 logical axioms that ROBOT
and Pellet report for SBMO 1.1; any difference aborts without writing.

Input:   ../../sbmo.rdf (or --tbox PATH)
Output:  sbm-ontology-dissertation/assets/ontology/tables/tbox-dl.tex
         (sibling dissertation repository; --stdout prints it instead)

Requirements (not stdlib): rdflib. Verified 2026-10-21 with rdflib 7.6.0.

Usage:  python3 tbox-dl-table.py
        python3 tbox-dl-table.py --stdout
"""
import argparse, collections, itertools, os, sys
import rdflib
from rdflib import RDF, RDFS, OWL, XSD, BNode
from rdflib.collection import Collection

HERE = os.path.dirname(os.path.abspath(__file__))
SBMO_ROOT = os.path.dirname(os.path.dirname(HERE))
DISSERTATION_ROOT = os.path.dirname(SBMO_ROOT)
OUT = os.path.join(DISSERTATION_ROOT, "sbm-ontology-dissertation", "assets",
                   "ontology", "tables", "tbox-dl.tex")
NS = "https://rafaelc-rb.github.io/sbmo#"
EXPECTED_LOGICAL_AXIOMS = 150  # SBMO 1.1 (ROBOT measure, Pellet info)
CENTRAL = "SoftwareBusinessModel"
EXAMPLE_SUBCLASS = ("SubscriptionRevenue", "RevenueSource")

ap = argparse.ArgumentParser()
ap.add_argument("--tbox", default=os.path.join(SBMO_ROOT, "sbmo.rdf"))
ap.add_argument("--stdout", action="store_true")
args = ap.parse_args()

g = rdflib.Graph()
g.parse(args.tbox, format="xml")
name = lambda u: str(u).split("#")[-1]
sf = lambda u: r"\mathsf{%s}" % name(u)  # DL rendering of a named entity


def fail(msg):
    sys.exit(f"tbox-dl-table: {msg}; nothing written")


# --- collect axioms by type -------------------------------------------------------
named_sub = []                    # (sub, super), both named classes
min_card = []                     # (class, property, filler)
for s, o in g.subject_objects(RDFS.subClassOf):
    if isinstance(o, BNode):
        n = g.value(o, OWL.minQualifiedCardinality)
        if g.value(o, RDF.type) != OWL.Restriction or n is None or int(n) != 1:
            fail(f"unexpected class expression under {name(s)}")
        min_card.append((s, g.value(o, OWL.onProperty), g.value(o, OWL.onClass)))
    else:
        named_sub.append((s, o))

defined = sorted(g.subjects(OWL.equivalentClass, None), key=name)
obj_props = sorted(g.subjects(RDF.type, OWL.ObjectProperty), key=name)
data_props = sorted(g.subjects(RDF.type, OWL.DatatypeProperty), key=name)
dom = {p: g.value(p, RDFS.domain) for p in obj_props + data_props}
rng = {p: g.value(p, RDFS.range) for p in obj_props + data_props}
if None in dom.values() or None in rng.values():
    fail("a property lacks a domain or a range")

disjoint = []                     # list of member lists, one per axiom
for a in g.subjects(RDF.type, OWL.AllDisjointClasses):
    disjoint.append(list(Collection(g, g.value(a, OWL.members))))
for s, o in g.subject_objects(OWL.disjointWith):
    disjoint.append([s, o])
between = [m for m in disjoint if any(name(c) == CENTRAL for c in m)]
within = [m for m in disjoint if m not in between]
if len(between) != 1:
    fail("expected one disjointness axiom over the central class and the dimensions")
pairs = lambda axioms: {frozenset(p) for m in axioms for p in itertools.combinations(m, 2)}

# no other logical construct may occur (property axioms, characteristics, ...)
allowed = {RDF.type, RDFS.subClassOf, RDFS.domain, RDFS.range, RDFS.label,
           RDFS.comment, OWL.equivalentClass, OWL.disjointWith, OWL.members,
           OWL.onProperty, OWL.onClass, OWL.minQualifiedCardinality,
           OWL.intersectionOf, OWL.unionOf, OWL.someValuesFrom, RDF.first,
           RDF.rest, OWL.versionIRI, OWL.versionInfo}
extra = {p for p in set(g.predicates()) - allowed
         if not (str(p).startswith("http://purl.org/dc/")
                 or (p, RDF.type, OWL.AnnotationProperty) in g)}
if extra:
    fail("unexpected predicates " + ", ".join(sorted(map(str, extra))))
types = {o for o in g.objects(None, RDF.type)}
if types - {OWL.Ontology, OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
            OWL.AnnotationProperty, OWL.Restriction, OWL.AllDisjointClasses}:
    fail("unexpected rdf:type values")

counts = collections.OrderedDict([
    ("Subsumption", len(named_sub)),
    ("Object property domain", len(obj_props)),
    ("Object property range", len(obj_props)),
    ("Data property domain", len(data_props)),
    ("Data property range", len(data_props)),
    ("Minimum cardinality", len(min_card)),
    ("Disjointness between dimensions", len(between)),
    ("Disjointness within dimensions", len(within)),
    ("Class definitions", len(defined)),
])
total = sum(counts.values())
if total != EXPECTED_LOGICAL_AXIOMS:
    fail(f"{total} logical axioms, expected {EXPECTED_LOGICAL_AXIOMS}")

# --- consistency with the text of Section 6.4.3 -----------------------------------
parents = {o for _, o in named_sub}
if any(not isinstance(o, BNode) for p in parents for o in g.objects(p, RDFS.subClassOf)):
    fail("a subclass parent is not a top-level class")
if (rdflib.URIRef(NS + EXAMPLE_SUBCLASS[0]), RDFS.subClassOf,
        rdflib.URIRef(NS + EXAMPLE_SUBCLASS[1])) not in g:
    fail("the example subsumption is not in the T-Box")
if {name(d) for p, d in dom.items() if p in data_props} != {CENTRAL}:
    fail("a data property has a domain other than " + CENTRAL)
n_between, n_within = len(pairs(between)), len(pairs(within))

# --- render -----------------------------------------------------------------------
def by_datatype():
    groups = collections.defaultdict(list)
    for p in data_props:
        groups[rng[p]].append(p)
    rows = []
    for dt in sorted(groups, key=lambda d: -len(groups[d])):
        ps = groups[dt]
        rows.append(r"$\top \sqsubseteq \forall U.\mathsf{xsd{:}%s}$ for $U \in \{%s\}$"
                    % (name(dt), r",\allowbreak\ ".join(sf(p) for p in ps)))
    return r" \newline ".join(rows)


central = [c for c in between[0] if name(c) == CENTRAL]
dims = central + sorted((c for c in between[0] if name(c) != CENTRAL), key=name)
card = collections.defaultdict(list)            # class -> [(property, filler)]
for c, p, f in sorted(min_card, key=lambda t: name(t[1])):
    card[c].append((p, f))
card_rows = []
for c in sorted(card, key=lambda c: (name(c) != CENTRAL, name(c))):
    if len(card[c]) == 1:
        (p, f), = card[c]
        card_rows.append(r"$%s \sqsubseteq {\geq}1\,%s.%s$" % (sf(c), sf(p), sf(f)))
    else:
        card_rows.append(r"$%s \sqsubseteq {\geq}1\,P.C$ for $P.C \in \{%s\}$" % (
            sf(c), r",\allowbreak\ ".join("%s.%s" % (sf(p), sf(f)) for p, f in card[c])))
card_rows = r" \newline ".join(card_rows)
sub_ex = r"$\mathsf{%s} \sqsubseteq \mathsf{%s}$" % EXAMPLE_SUBCLASS

rows = [
    ("Subsumption",
     r"$C \sqsubseteq D$ for each subclass $C$ of a top-level class $D$ "
     r"(Table~\ref{tab:subclasses}), \textit{e.g.}, " + sub_ex),
    ("Object property domain",
     r"$\exists P.\top \sqsubseteq D_P$ for each object property $P$ with domain $D_P$ "
     r"(Table~\ref{tab:object_properties})"),
    ("Object property range",
     r"$\top \sqsubseteq \forall P.R_P$ for each object property $P$ with range $R_P$ "
     r"(Table~\ref{tab:object_properties})"),
    ("Data property domain",
     r"$\exists U.\top \sqsubseteq \mathsf{%s}$ for each data property $U$ "
     r"(Section~\ref{subsec:ontology_attributes})" % CENTRAL),
    ("Data property range", by_datatype()),
    ("Minimum cardinality", card_rows),
    ("Disjointness between dimensions",
     r"$C_i \sqcap C_j \sqsubseteq \bot$ for $i \neq j$, with $C_i, C_j \in \{%s\}$ "
     r"(%d pairs)" % (r",\allowbreak\ ".join(sf(c) for c in dims), n_between)),
    ("Disjointness within dimensions",
     r"%d pairs of subclasses of the same dimension (Section~\ref{subsec:axioms})" % n_within),
    ("Class definitions",
     r"%s (Section~\ref{subsec:axioms})" % ", ".join("$%s$" % sf(c) for c in defined)),
]

lines = [
    "% Generated by sbmo/validation/scripts/tbox-dl-table.py from sbmo.rdf -- do not edit by hand.",
    r"\rowcolors{1}{white}{gray!20}",
    r"\begin{table}[!htb]",
    r"\renewcommand{\arraystretch}{1.3}",
    r"\caption[Logical axioms of the SBMO T-Box in description logic notation]"
    r"{Logical axioms of the SBMO T-Box in description logic notation, by type. "
    r"$P$ ranges over object properties and $U$ over data properties; "
    r"the last column gives the number of OWL axioms of each type.}",
    r"\label{tab:tbox_dl}",
    r"\centering",
    r"\small",
    r"\begin{tabular}{>{\raggedright\arraybackslash}p{3.1cm}|"
    r">{\raggedright\arraybackslash}p{10.4cm}|r}",
    r"\bottomrule",
    r"\rowcolor{gray!50}",
    r"\textbf{Axiom Type} & \textbf{Axioms in DL} & \textbf{No.} \\",
    r"\hline",
]
for (label, cell) in rows:
    lines.append(f"{label} & {cell} & {counts[label]} \\\\")
lines += [
    r"\hline",
    r"\textbf{Total} & & \textbf{%d} \\" % total,
    r"\toprule",
    r"\end{tabular}",
    r"\fonte{the author.}",
    r"\end{table}",
]
tex = "\n".join(lines) + "\n"

summary = ", ".join(f"{k} {v}" for k, v in counts.items())
print(f"tbox-dl-table: {summary}; total {total}; disjoint pairs "
      f"{n_between} + {n_within} = {n_between + n_within}", file=sys.stderr)
if args.stdout:
    sys.stdout.write(tex)
else:
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(tex)
    print(f"tbox-dl-table: wrote {OUT}", file=sys.stderr)
