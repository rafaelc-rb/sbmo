// SBMO validation: prints Pellet justifications (explanations) of one entailment.
//
//   java -cp <dir>:<pellet jars> Justify instance <file> <individualIRI> <classIRI> <max>
//   java -cp <dir>:<pellet jars> Justify subclass <file> <subClassIRI> <superClassIRI> <max>
//   java -cp <dir>:<pellet jars> Justify inconsistent <file> <max>
//
// Output: one line per axiom, tab-separated: J<n>, axiom type, Manchester syntax,
// DL syntax ("NONE" if the entailment does not hold). Compiled and run by
// reasoning-demo.py against the Pellet 2.3.1 / OWL API 3.4.3 jars bundled with
// owlready2. It calls Pellet's explanation API directly because the renderer of
// the Pellet 2.3.1 command-line "explain" crashes on unions nested inside
// intersections (as in NetworkedPlatformModel).
import java.io.File;
import java.util.*;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.util.SimpleShortFormProvider;
import uk.ac.manchester.cs.owl.owlapi.mansyntaxrenderer.ManchesterOWLSyntaxOWLObjectRendererImpl;
import uk.ac.manchester.cs.owlapi.dlsyntax.DLSyntaxObjectRenderer;
import com.clarkparsia.pellet.owlapiv3.PelletReasoner;
import com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory;
import com.clarkparsia.owlapi.explanation.PelletExplanation;

public class Justify {
    public static void main(String[] a) throws Exception {
        PelletExplanation.setup();
        OWLOntologyManager m = OWLManager.createOWLOntologyManager();
        OWLOntology o = m.loadOntologyFromOntologyDocument(new File(a[1]));
        OWLDataFactory f = m.getOWLDataFactory();
        PelletReasoner r = PelletReasonerFactory.getInstance().createNonBufferingReasoner(o);
        PelletExplanation e = new PelletExplanation(r);
        int max = Integer.parseInt(a[a.length - 1]);
        Set<Set<OWLAxiom>> just;
        switch (a[0]) {
            case "instance":
                just = e.getInstanceExplanations(f.getOWLNamedIndividual(IRI.create(a[2])),
                        f.getOWLClass(IRI.create(a[3])), max);
                break;
            case "subclass":
                just = e.getSubClassExplanations(f.getOWLClass(IRI.create(a[2])),
                        f.getOWLClass(IRI.create(a[3])), max);
                break;
            default:
                just = e.getInconsistencyExplanations(max);
        }
        ManchesterOWLSyntaxOWLObjectRendererImpl man = new ManchesterOWLSyntaxOWLObjectRendererImpl();
        DLSyntaxObjectRenderer dl = new DLSyntaxObjectRenderer();
        dl.setShortFormProvider(new SimpleShortFormProvider());
        // Sort justifications by size, then axioms by type and text, so the output is stable.
        List<List<String[]>> rows = new ArrayList<>();
        for (Set<OWLAxiom> j : just) {
            List<String[]> js = new ArrayList<>();
            for (OWLAxiom ax : j)
                js.add(new String[] {ax.getAxiomType().getName(),
                        man.render(ax).replaceAll("\\s+", " "), dl.render(ax)});
            js.sort(Comparator.comparing((String[] x) -> x[0]).thenComparing(x -> x[1]));
            rows.add(js);
        }
        rows.sort(Comparator.comparing((List<String[]> x) -> x.size())
                .thenComparing(x -> String.join("|", x.stream().map(y -> y[1]).toList())));
        int n = 0;
        for (List<String[]> js : rows) {
            n++;
            for (String[] x : js)
                System.out.println("J" + n + "\t" + x[0] + "\t" + x[1] + "\t" + x[2]);
        }
        if (n == 0) System.out.println("NONE");
    }
}
