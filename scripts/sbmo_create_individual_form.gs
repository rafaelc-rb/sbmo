/**
 * SBMO Validation Form — Google Apps Script
 *
 * Cria Google Forms alinhados com a ontologia SBMO (sbmo.rdf) para coletar
 * dados de modelos de negócio de software de empresas reais.
 *
 * Há duas localizações: `pt` (padrão) e `en`.
 *
 * Uso:
 *   1. Abra https://script.google.com e crie um novo projeto.
 *   2. Cole este arquivo inteiro no Code.gs.
 *   3. Execute:
 *        - `createSBMOValidationFormAll()` — cria o formulário em PT e em EN (ver logs);
 *        - ou `createSBMOValidationFormPT()` / `createSBMOValidationFormEN()`.
 *   4. Verifique os logs (View > Logs) para as URLs.
 *   Cada execução cria novos Formulários no Google Drive: guarde a URL alvo e evite
 *   rodar de novo em produção, para não acumular cópias de teste.
 *
 * Cada seção mapeia uma dimensão da ontologia. Perguntas obrigatórias
 * correspondem a propriedades com minQualifiedCardinality >= 1.
 *
 * Antes de publicar: confira os e-mails em SBMO_RESEARCH_CONFIG (institucionais abaixo).
 */

/**
 * Contato exibido no TCLE, no ICF (EN) e na mensagem de confirmação.
 * Corrigido em 2026-08-18 para bater com o formulário real efetivamente
 * publicado (conferido contra um PDF exportado pelo autor), que usa os
 * e-mails institucionais abaixo, não o Gmail pessoal usado numa versão
 * anterior deste script. Ver sbmo/validation/zenodo-package/informed_consent/
 * para a transcrição verbatim verificada.
 * @type {{ researcherEmail: string, advisorEmail: string }}
 */
var SBMO_RESEARCH_CONFIG = {
	/** E-mail institucional do pesquisador (aluno). */
	researcherEmail: "rafaelcardoso.aluno@unipampa.edu.br",
	/** E-mail institucional do orientador. */
	advisorEmail: "bernardino@unipampa.edu.br",
};

/**
 * Texto do TCLE (pt-BR), corrigido em 2026-08-18 para ser uma transcrição
 * verbatim do formulário real efetivamente publicado (ver
 * sbmo/validation/zenodo-package/informed_consent/informed_consent_pt.md).
 * Os e-mails vêm de SBMO_RESEARCH_CONFIG.
 */
function tcleTextPT_() {
	var cfg = SBMO_RESEARCH_CONFIG;
	var core =
		"Você está sendo convidado(a) a participar da pesquisa vinculada a uma dissertação de " +
		"mestrado do Programa de Pós-Graduação em Engenharia de Software (PPGES) da UNIPAMPA, " +
		"com o objetivo de coletar informações sobre modelos de negócio de software para " +
		"validar a Software Business Model Ontology (SBMO).\n\n" +
		"Procedimentos: a participação consiste no preenchimento deste formulário (tempo estimado: " +
		"15–20 minutos). A coleta de e-mail, se exibida, destina-se a contato acadêmico, conforme a " +
		"configuração do Google Forms.\n\n" +
		"Riscos e Desconfortos: todas as medidas serão tomadas durante a coleta de dados para " +
		"garantir sua privacidade e anonimato. Além disso, não há riscos ou desconfortos que possam " +
		"afetá-lo(a) durante o estudo, exceto problemas comuns como fadiga, estresse ou leve mal-estar.\n\n" +
		"Benefícios: a pesquisa pode contribuir para o avanço de descrições ontológicas de modelos " +
		"de negócio de software. Este estudo também fornecerá resultados relevantes para o grupo de " +
		"pesquisa LESSE. Você não incorrerá em quaisquer custos ou encargos para participar do " +
		"estudo, nem receberá qualquer reembolso ou compensação por autorizar o uso de seus dados " +
		"na pesquisa.\n\n" +
		"Confidencialidade: as respostas serão tratadas de forma confidencial e utilizadas " +
		"agregadas para fins científicos, de modo a evitar identificação indevida de pessoas ou " +
		"empresas, salvo autorização explícita.\n\n" +
		"Voluntariedade: sua participação neste estudo é muito importante e voluntária, pois requer " +
		"sua aprovação para o uso dos dados coletados. De acordo com a Resolução CNS nº 466/2012 do " +
		"Conselho Nacional de Saúde (CNS), o respeito à dignidade humana exige que toda pesquisa " +
		"seja conduzida somente com consentimento livre e esclarecido. Você tem o direito de recusar " +
		"a participação ou desistir deste estudo a qualquer momento, sem penalidades. Caso decida " +
		"desistir, por favor, notifique o pesquisador responsável.\n\n" +
		"Esclarecimentos: Os pesquisadores estarão disponíveis para fornecer esclarecimentos e " +
		"responder a quaisquer perguntas.\n" +
		"Pesquisador: Rafael Ribeiro Cardoso - " + cfg.researcherEmail + "\n" +
		"Orientador: Prof. Dr. Maicon Bernardino da Silveira - " + cfg.advisorEmail;
	return core;
}

/**
 * Informed Consent (EN). NÃO VERIFICADO contra um formulário em inglês
 * publicado: é uma tradução best-effort do texto em PT acima. Não há
 * evidência de que a variante em inglês deste formulário tenha sido
 * publicada; as 31 respostas reais usam apenas o formulário em português.
 * Os e-mails vêm de SBMO_RESEARCH_CONFIG.
 */
function tcleTextEN_() {
	var cfg = SBMO_RESEARCH_CONFIG;
	var core =
		"You are invited to take part in research associated with a master's thesis at the " +
		"Postgraduate Program in Software Engineering (PPGES), Federal University of Pampa " +
		"(UNIPAMPA), Brazil. The study collects information about software business models to " +
		"validate the Software Business Model Ontology (SBMO).\n\n" +
		"Procedures: participation consists of completing this form (estimated time: 15-20 minutes). " +
		"If the form is configured to collect e-mail, it is used for academic follow-up, per Google Forms settings.\n\n" +
		"Risks and Discomforts: every measure will be taken during data collection to protect your " +
		"privacy and anonymity. No risks or discomfort are otherwise expected during the study beyond " +
		"common issues such as fatigue, stress, or mild discomfort.\n\n" +
		"Benefits: the research may help advance ontological descriptions of software business " +
		"models. This study will also produce results relevant to the LESSE research group. You will " +
		"incur no costs to take part, nor receive any reimbursement or compensation for authorizing " +
		"the use of your data.\n\n" +
		"Confidentiality: responses are treated as confidential and used in aggregate for scientific " +
		"purposes, avoiding undue identification of individuals or organizations unless explicitly authorized.\n\n" +
		"Voluntary participation: your participation is very important and voluntary, as it requires " +
		"your approval for the use of the collected data. Per Resolution CNS 466/2012 of the Brazilian " +
		"National Health Council (CNS), respect for human dignity requires that all research be " +
		"conducted only with free and informed consent. You have the right to decline or withdraw " +
		"from this study at any time, without penalty. If you decide to withdraw, please notify the " +
		"responsible researcher.\n\n" +
		"Contact: the researchers are available to provide clarification and answer any questions.\n" +
		"Researcher: Rafael Ribeiro Cardoso - " + cfg.researcherEmail + "\n" +
		"Advisor: Prof. Dr. Maicon Bernardino da Silveira - " + cfg.advisorEmail;
	return core;
}

/**
 * @param {string} locale 'pt' | 'en'
 * @return {Object} all user-visible strings for the form
 */
function getFormStrings_(locale) {
	var isEn = locale === "en";
	function L(/** string */ en, /** string */ pt) {
		return isEn ? en : pt;
	}
	return {
		formTitle: L(
			"SBMO — Software Business Model Validation",
			"SBMO — Validação de Modelo de Negócio de Software",
		),
		formDescription: L(
			// EN: not independently verified, see tcleTextEN_ note above.
			"This questionnaire is part of a master's thesis (PPGES/UNIPAMPA) and supports " +
				"validating the Software Business Model Ontology (SBMO). Responses are confidential " +
				"and used exclusively for academic purposes.\n\n" +
				"The research targets people with practical knowledge of a software product, such as " +
				"founders, CEOs, product leaders, business leaders, or professionals with a clear view " +
				"of how the software generates revenue, delivers value, reaches customers, and " +
				"positions itself in the market.\n\n" +
				"The Informed Consent form appears at the start of the questionnaire, followed by the " +
				"research questions. Estimated time: 15 to 20 minutes.",
			// PT: verbatim, confirmado em 2026-08-18 contra o formulário real publicado.
			"Este questionário faz parte de uma dissertação de mestrado do PPGES/UNIPAMPA e " +
				"apoia a validação da Software Business Model Ontology (SBMO). As respostas são " +
				"confidenciais e utilizadas exclusivamente para fins acadêmicos.\n\n" +
				"A pesquisa é destinada a pessoas que conhecem bem algum produto de software na " +
				"prática, como fundadores, CEOs, líderes de produto, líderes de negócio ou " +
				"profissionais com visão clara sobre como o software gera receita, entrega valor, " +
				"chega aos clientes e se posiciona no mercado.\n\n" +
				"O Termo de Consentimento Livre e Esclarecido aparece no início do formulário. Em " +
				"seguida, são apresentadas as perguntas da pesquisa. Tempo estimado de resposta: 15 a " +
				"20 minutos.",
		),
		confirmation: L(
			"Thank you for your participation! Your answers will be used only for academic research in the context of SBMO validation.\n\n" +
				"Questions: " +
				SBMO_RESEARCH_CONFIG.researcherEmail,
			"Obrigado pela sua participação! Suas respostas serão utilizadas exclusivamente para pesquisa " +
				"acadêmica no contexto da validação da SBMO.\n\n" +
				"Dúvidas: " +
				SBMO_RESEARCH_CONFIG.researcherEmail,
		),

		tcleSectionTitle: L(
			"Informed Consent (ICF)",
			"Termo de Consentimento Livre e Esclarecido (TCLE)",
		),
		tcleBody: isEn ? tcleTextEN_() : tcleTextPT_(),
		consentItemTitle: L("Participation", "Participação"),
		consentCheckbox: L(
			// EN: not independently verified, see tcleTextEN_ note above.
			"Consent Declaration: I declare that I have read and agree with the information in this " +
				"document, and that all technical language used to describe this research study was " +
				"satisfactorily explained, with all my questions answered. I also confirm that I " +
				"received a copy of this Informed Consent Form and understand that I may revoke " +
				"authorization for the use of my data in this study at any time, without any penalty. " +
				"I voluntarily agree to take part in this study.",
			// PT: verbatim, confirmado em 2026-08-18 contra o formulário real publicado.
			"Declaração de Consentimento: Declaro que li e concordo com as informações contidas " +
				"neste documento e que toda a linguagem técnica utilizada na descrição deste estudo " +
				"de pesquisa foi satisfatoriamente explicada, com todas as minhas dúvidas respondidas. " +
				"Confirmo também que recebi uma cópia deste Termo de Consentimento Livre e Esclarecido " +
				"(TCLE) e compreendo que posso revogar a autorização para o uso dos meus dados neste " +
				"estudo a qualquer momento, sem qualquer penalidade. Concordo voluntariamente em " +
				"participar deste estudo.",
		),

		s1Title: L(
			"1. Company and product identification",
			"1. Identificação da Empresa e do Produto",
		),
		s1Help: L(
			"Basic information to identify the company and its main software product or service.",
			"Informações básicas para identificar a empresa e seu principal produto ou serviço de software.",
		),
		company: L("Company name", "Nome da empresa"),
		companyHelp: L("Official name of the company.", "Nome oficial da empresa."),
		product: L("Product or service name", "Nome do produto ou serviço"),
		productHelp: L(
			"Name of the main software product or service you offer.",
			"Nome do principal produto ou serviço de software oferecido.",
		),
		year: L("Launch year", "Ano de lançamento"),
		yearHelp: L(
			"Year the product/service was first launched or made available (e.g. 2018).",
			"Ano em que o produto/serviço foi lançado ou disponibilizado pela primeira vez (ex.: 2018).",
		),
		bmodel: L(
			"Brief description of the business model",
			"Descrição breve do modelo de negócio",
		),
		bmodelHelp: L(
			"In 2–4 sentences, describe how this product/service creates value and revenue. " +
				"Example: “We offer a B2B SaaS for project management, sold via monthly subscription with a free tier for small teams.”",
			"Em 2 a 4 frases, descreva como esse produto/serviço gera valor e receita. " +
				'Exemplo: "Oferecemos uma plataforma SaaS B2B para gestão de projetos, vendida por assinaturas ' +
				'mensais com um plano gratuito para equipes pequenas."',
		),
		respondent: L("Respondent’s name and role", "Nome e cargo do respondente"),
		respondentHelp: L(
			"Your name and role in the company (e.g. “Alex Smith, CTO”).",
			'Seu nome e cargo na empresa (ex.: "João Silva, CTO").',
		),
		operational: L(
			"Is the business model of this product/service already operational?",
			"O modelo de negócio deste produto/serviço já está operacional?",
		),
		operationalHelp: L(
			"If you select “No” or “Partially”, please answer the remaining questions based on the planned scenario for the next 12 months.",
			"Se marcar “Não” ou “Parcialmente”, responda as demais perguntas com base no cenário planejado para os próximos 12 meses.",
		),
		opYes: L("Yes", "Sim"),
		opNo: L("No", "Não"),
		opPartial: L("Partially", "Parcialmente"),

		s2Title: L(
			"2. Type of product or service",
			"2. Tipo de Produto ou Serviço",
		),
		s2Help: L(
			"What type of product or service does the company offer?\n" +
				"Select all that apply. At least one option is required.",
			"Que tipo de produto ou serviço a empresa oferece?\n" +
				"Selecione todas as opções que se aplicam. Pelo menos uma opção é obrigatória.",
		),
		s2Q: L("Type of product or service", "Tipo de produto ou serviço"),
		s2QHelp: L(
			"Select all types that describe your offering.",
			"Selecione todos os tipos que descrevem sua oferta.",
		),
		s2Other: L(
			"Other type (if applicable)",
			"Outro tipo de produto/serviço (se aplicável)",
		),
		s2OtherHelp: L(
			"If you selected “Other” above, specify here.",
			'Se selecionou "Outro" acima, especifique aqui.',
		),

		s3Title: L("3. Delivery mode", "3. Modo de Entrega"),
		s3Help: L(
			"How is the software delivered to customers?\n" +
				"Select all that apply.",
			"Como o software é entregue aos clientes?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s3Q: L("Delivery mode", "Modo de entrega"),
		s3Other: L(
			"Other delivery mode (if applicable)",
			"Outro modo de entrega (se aplicável)",
		),

		s4Title: L("4. Revenue sources", "4. Fontes de Receita"),
		s4Help: L(
			"How does the product/service generate revenue?\n" +
				"Select all that apply.",
			"Como o produto/serviço gera receita?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s4Q: L("Revenue sources", "Fontes de receita"),
		s4Other: L(
			"Other revenue source (if applicable)",
			"Outra fonte de receita (se aplicável)",
		),

		s5Title: L("5. Pricing strategy", "5. Estratégia de Precificação"),
		s5Help: L(
			"What pricing strategy does the product/service use?\n" +
				"Select all that apply.",
			"Qual estratégia de precificação o produto/serviço utiliza?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s5Q: L("Pricing strategy", "Estratégia de precificação"),
		s5Other: L(
			"Other pricing strategy (if applicable)",
			"Outra estratégia de precificação (se aplicável)",
		),
		s5Period: L("Billing cadence", "Periodicidade de cobrança"),
		s5PeriodHelp: L(
			"How often are customers charged? (e.g. monthly, annual, per transaction)",
			"Com que frequência os clientes são cobrados? (ex.: mensal, anual, por transação)",
		),
		s5Desc: L("Pricing description", "Descrição da precificação"),
		s5DescHelp: L(
			"If pricing has nuances not captured above, describe here. " +
				"Example: “We have 3 plans — Free, Pro ($99/mo), Enterprise (custom).”",
			"Se o modelo de precificação tem nuances não capturadas acima, descreva aqui. " +
				'Exemplo: "Temos 3 planos — Grátis, Pro (R$99/mês), Enterprise (preço sob consulta)."',
		),

		s6Title: L("6. Customer type", "6. Tipo de Cliente"),
		s6Help: L(
			"Who are the main customers?\n" + "Select all that apply.",
			"Quem são os principais clientes?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s6Q: L("Customer type", "Tipo de cliente"),
		s6Other: L(
			"Other customer type (if applicable)",
			"Outro tipo de cliente (se aplicável)",
		),

		s7Title: L("7. Ecosystem role", "7. Papel no Ecossistema"),
		s7Help: L(
			"What role does the product/service play in your ecosystem?\n" +
				"Select all that apply.",
			"Qual papel o produto/serviço desempenha no seu ecossistema?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s7Q: L("Ecosystem role", "Papel no ecossistema"),
		s7Other: L(
			"Other ecosystem role (if applicable)",
			"Outro papel no ecossistema (se aplicável)",
		),

		s8Title: L("8. Acquisition channel", "8. Canal de Aquisição"),
		s8Help: L(
			"How do customers discover and start using the product/service?\n" +
				"Select all that apply.",
			"Como os clientes descobrem e começam a usar o produto/serviço?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s8Q: L("Acquisition channel", "Canal de aquisição"),
		s8Other: L(
			"Other acquisition channel (if applicable)",
			"Outro canal de aquisição (se aplicável)",
		),

		s9Title: L(
			"9. Intellectual property",
			"9. Regime de Propriedade Intelectual",
		),
		s9Help: L(
			"What is the licensing or IP model? Select all that apply. This section is optional.",
			"Qual o modelo de licenciamento ou propriedade intelectual do software?\n" +
				"Selecione todas as opções que se aplicam. Esta seção é opcional.",
		),
		s9Q: L("IP / licensing", "Regime de propriedade intelectual"),
		s9Other: L(
			"Other IP regime (if applicable)",
			"Outro regime de PI (se aplicável)",
		),

		s10Title: L("10. Base pricing unit", "10. Unidade Base de Precificação"),
		s10Help: L(
			"What base metric is used to charge customers? Select all that apply. Optional section.",
			"Qual é a métrica base usada para cobrar os clientes?\n" +
				"Selecione todas as opções que se aplicam. Esta seção é opcional.",
		),
		s10Q: L("Base pricing unit", "Unidade base de precificação"),
		s10Other: L(
			"Other base unit (if applicable)",
			"Outra unidade base de precificação (se aplicável)",
		),

		s11Title: L("11. Network effects", "11. Efeitos de Rede"),
		s11Help: L(
			"Does the product/service benefit from network effects? Select all that apply. Optional section.",
			"O produto/serviço se beneficia de efeitos de rede?\n" +
				"Selecione todas as opções que se aplicam. Esta seção é opcional.",
		),
		s11Q: L("Type of network effect", "Tipo de efeito de rede"),
		s11Other: L(
			"Other network effect (if applicable)",
			"Outro tipo de efeito de rede (se aplicável)",
		),

		s12Title: L("12. Success factors", "12. Fatores de Sucesso"),
		s12Help: L(
			"What factors are critical to the success of this business model? Select all that apply.",
			"Quais fatores você considera críticos para o sucesso deste modelo de negócio?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s12Q: L("Success factors", "Fatores de sucesso"),
		s12Other: L(
			"Other success factor (if applicable)",
			"Outro fator de sucesso (se aplicável)",
		),

		s13Title: L(
			"13. Implementation challenges",
			"13. Desafios de Implementação",
		),
		s13Help: L(
			"What challenges has the company faced when implementing or evolving this business model? Select all that apply.",
			"Quais desafios a empresa enfrentou ao implementar ou evoluir este modelo de negócio?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s13Q: L("Implementation challenges", "Desafios de implementação"),
		s13Other: L(
			"Other challenge (if applicable)",
			"Outro desafio (se aplicável)",
		),

		s14Title: L("14. Mitigation strategies", "14. Estratégias de Mitigação"),
		s14Help: L(
			"If challenges were identified, what strategies has the company used? Select all that apply.",
			"Se desafios foram identificados acima, quais estratégias a empresa usou para enfrentá-los?\n" +
				"Selecione todas as opções que se aplicam.",
		),
		s14Q: L("Mitigation strategies", "Estratégias de mitigação"),
		s14Other: L(
			"Other mitigation (if applicable)",
			"Outra estratégia de mitigação (se aplicável)",
		),
		s14Map: L(
			"Which challenge does each mitigation address?",
			"Qual desafio cada mitigação endereça?",
		),
		s14MapHelp: L(
			"If possible, map each strategy to a challenge. " +
				"Example: “Flexible pricing → revenue stream transition; Pilot → security.”",
			"Se possível, indique qual desafio cada estratégia selecionada busca resolver. " +
				'Exemplo: "Precificação flexível → Transformação de fluxo de receita; Piloto → Segurança"',
		),

		s15Title: L("15. Additional comments", "15. Comentários Adicionais"),
		s15Help: L(
			"Any further information you want to share about the business model.",
			"Qualquer informação adicional que queira compartilhar sobre o modelo de negócio.",
		),
		s15Q: L(
			"Comments or additional notes",
			"Comentários ou observações adicionais",
		),
		s15QHelp: L(
			"Is there any aspect of your software business model that was not covered? Any important dimension you missed?",
			"Existe algum aspecto do modelo de negócio de software da sua empresa que não foi " +
				"coberto pelas perguntas acima? Alguma dimensão que você considera importante e que estava faltando?",
		),
		s15Follow: L(
			"Would you be available for a short follow-up call (15–20 min) to clarify answers?",
			"Você estaria disponível para uma breve conversa de acompanhamento (15–20 min) para esclarecer respostas?",
		),
		s15Y: L("Yes", "Sim"),
		s15N: L("No", "Não"),
		s15M: L("Maybe", "Talvez"),
	};
}

/**
 * Choice lists per locale (product type, delivery, …).
 * @param {string} locale 'pt' | 'en'
 */
function getChoiceGroups_(locale) {
	var isEn = locale === "en";
	if (isEn) {
		return {
			s2: [
				"Application (standalone software application)",
				"Platform (development or business platform)",
				"Managed service (hosted and operated by you on the customer’s behalf)",
				"API service (functionality exposed via an API)",
				"Data product (data, analytics, or insights as the core offering)",
				"Infrastructure (cloud, hosting, compute)",
				"SDK / developer kit (libraries, frameworks, or tools for developers)",
				"Other (specify in the next item)",
			],
			s3: [
				"SaaS multi-tenant (shared infrastructure, browser access)",
				"SaaS single-tenant (dedicated instance per customer)",
				"On‑premises (installed on the customer’s infrastructure)",
				"Mobile delivery (native mobile app)",
				"Desktop delivery (native desktop app)",
				"Hybrid delivery (cloud and on‑premises combined)",
				"Other (specify in the next item)",
			],
			s4: [
				"Subscription revenue (recurring periodic payments)",
				"Usage/consumption revenue (pay for what you use)",
				"Transaction revenue (fee per transaction processed)",
				"Advertising revenue",
				"Perpetual license (one-time licensing fee)",
				"Support revenue (paid support, consulting, or training)",
				"Marketplace take rate (commission on third‑party sales)",
				"Open core (free core + paid premium features)",
				"Dual licensing (open source + commercial license)",
				"Other (specify in the next item)",
			],
			s5: [
				"Subscription pricing (fixed periodic fee)",
				"Pay-as-you-go pricing (usage-based billing)",
				"Freemium (free plan + paid upgrades)",
				"Value-based pricing (price tied to perceived value or outcomes)",
				"Cost-based pricing (price from cost + margin)",
				"Other (specify in the next item)",
			],
			s6: [
				"B2B (selling to other businesses)",
				"B2C (selling to end consumers)",
				"SMEs (small and medium businesses)",
				"Enterprise (large organizations)",
				"Government (public sector)",
				"Developer tools (developers or technical teams as end users)",
				"Other (specify in the next item)",
			],
			s7: [
				"Standalone product (independent, self-contained)",
				"Two-sided platform (connects two distinct user groups)",
				"Marketplace (facilitates transactions between buyers and sellers)",
				"OEM component (embedded in other companies’ products)",
				"Plugin / add-on (extends another platform’s functionality)",
				"Other (specify in the next item)",
			],
			s8: [
				"Direct sales (sales team, outbound)",
				"Product-led growth (self-serve sign-up, free trial)",
				"Partner channel (resellers, distributors, integrators)",
				"Digital marketing (SEO, ads, content, social media)",
				"Marketplace channel (app stores or software marketplaces)",
				"Referral (word of mouth, referral programs)",
				"Other (specify in the next item)",
			],
			s9: [
				"Proprietary (closed source, all rights reserved)",
				"Permissive open source (MIT, Apache, BSD)",
				"Open source (broad, community-driven)",
				"Dual license (open source + commercial license)",
				"Open core (open source core + proprietary extensions)",
				"Copyleft (GPL, AGPL)",
				"Other (specify in the next item)",
			],
			s10: [
				"User / license (per user or seat pricing)",
				"Transaction-based (per transaction pricing)",
				"Compute time (per hour of processing or CPU)",
				"Revenue share (percentage of customer revenue)",
				"API calls (per API request pricing)",
				"Storage (per GB or TB stored)",
				"Device (per connected device pricing)",
				"Other (specify in the next item)",
			],
			s11: [
				"Direct network effect (more users = more value for each user)",
				"Cross-side network effect (more on one side = more value for the other side)",
				"Data-driven effect (more data = better product/service)",
				"No significant network effects",
				"Other (specify in the next item)",
			],
			s12: [
				"Ecosystem management (partners, integrations, developer community)",
				"Market expansion (geographic or new segments)",
				"Service quality (reliability, performance, support quality)",
				"Organizational readiness (team skills, processes, internal readiness)",
				"Value focus (delivering measurable value to the customer)",
				"Other (specify in the next item)",
			],
			s13: [
				"Security concerns (data protection, compliance, vulnerabilities)",
				"Revenue stream transformation (switching pricing or revenue models)",
				"Customer trust (transparency, reliability, retention)",
				"Partner ecosystem disruption (resellers, integrators impact)",
				"Organizational readiness (internal resistance, skill gaps)",
				"Quality management (quality during scale or transitions)",
				"Other (specify in the next item)",
			],
			s14: [
				"Flexible pricing (adjust prices to reduce churn or attract segments)",
				"Hybrid model (combine delivery or revenue models for gradual transition)",
				"Pilot implementation (test changes with a subset of customers first)",
				"Partner compensation (incentives or support to reduce partner disruption)",
				"Other (specify in the next item)",
			],
		};
	}
	return {
		s2: [
			"Aplicação (software aplicativo independente)",
			"Plataforma (plataforma de desenvolvimento ou negócios)",
			"Serviço gerenciado (hospedado e operado por vocês em nome do cliente)",
			"Serviço de API (funcionalidade exposta via API)",
			"Produto de dados (dados, analytics ou insights como oferta principal)",
			"Infraestrutura (infraestrutura cloud, hospedagem, computação)",
			"SDK / Kit de desenvolvimento (bibliotecas, frameworks ou ferramentas para desenvolvedores)",
			"Outro (especifique no campo seguinte)",
		],
		s3: [
			"SaaS multi-tenant (infraestrutura compartilhada, acesso via navegador)",
			"SaaS single-tenant (instância dedicada por cliente)",
			"On-premises (instalado na infraestrutura do próprio cliente)",
			"Entrega mobile (aplicativo móvel nativo)",
			"Entrega desktop (aplicativo desktop nativo)",
			"Entrega híbrida (combinação de cloud e on-premises)",
			"Outro (especifique no campo seguinte)",
		],
		s4: [
			"Receita por assinatura (pagamentos periódicos recorrentes)",
			"Receita por uso/consumo (pague pelo que usar)",
			"Receita por transação (taxa por transação processada)",
			"Receita por publicidade",
			"Receita por licença perpétua (taxa única de licenciamento)",
			"Receita por suporte (suporte pago, consultoria ou treinamento)",
			"Taxa de marketplace (comissão sobre vendas de terceiros)",
			"Receita open core (núcleo gratuito + funcionalidades premium pagas)",
			"Receita por licenciamento dual (código aberto + licença comercial)",
			"Outro (especifique no campo seguinte)",
		],
		s5: [
			"Precificação por assinatura (taxa periódica fixa)",
			"Precificação pay-as-you-go (cobrança baseada em uso)",
			"Precificação freemium (plano gratuito + upgrades pagos)",
			"Precificação baseada em valor (preço atrelado ao valor percebido ou resultados)",
			"Precificação baseada em custo (preço derivado do custo mais margem)",
			"Outro (especifique no campo seguinte)",
		],
		s6: [
			"B2B (venda para outras empresas)",
			"B2C (venda para consumidores finais)",
			"PMEs (pequenas e médias empresas)",
			"Enterprise (grandes organizações)",
			"Governo (setor público)",
			"Ferramentas para desenvolvedores (desenvolvedores ou equipes técnicas como usuários finais)",
			"Outro (especifique no campo seguinte)",
		],
		s7: [
			"Produto standalone (independente, autocontido)",
			"Plataforma bilateral (conecta dois grupos distintos de usuários)",
			"Marketplace (facilita transações entre vendedores e compradores)",
			"Componente OEM (embutido em produtos de outras empresas)",
			"Plugin / complemento (estende a funcionalidade de outra plataforma)",
			"Outro (especifique no campo seguinte)",
		],
		s8: [
			"Venda direta (equipe de vendas, outbound)",
			"Crescimento liderado pelo produto (cadastro self-service, free trial)",
			"Canal de parceiros (revendedores, distribuidores, integradores)",
			"Marketing digital (SEO, anúncios, marketing de conteúdo, redes sociais)",
			"Canal de marketplace (listado em app stores ou marketplaces de software)",
			"Indicação (boca a boca, programas de referral)",
			"Outro (especifique no campo seguinte)",
		],
		s9: [
			"Proprietário (código fechado, todos os direitos reservados)",
			"Open source permissivo (MIT, Apache, BSD)",
			"Open source (geral, orientado à comunidade)",
			"Licença dual (código aberto + licença comercial)",
			"Open core (núcleo open source + extensões proprietárias)",
			"Copyleft (GPL, AGPL)",
			"Outro (especifique no campo seguinte)",
		],
		s10: [
			"Usuário / licença (preço por usuário ou assento)",
			"Baseado em transação (preço por transação)",
			"Tempo de computação (preço por hora de processamento ou CPU)",
			"Compartilhamento de receita (percentual da receita do cliente)",
			"Chamadas de API (preço por requisição de API)",
			"Armazenamento (preço por GB ou TB armazenado)",
			"Dispositivo (preço por dispositivo conectado)",
			"Outro (especifique no campo seguinte)",
		],
		s11: [
			"Efeito de rede direto (mais usuários = mais valor para cada usuário)",
			"Efeito de rede cruzado (mais usuários de um lado = mais valor para o outro lado)",
			"Efeito de rede orientado a dados (mais dados = melhor produto/serviço)",
			"Sem efeitos de rede significativos",
			"Outro (especifique no campo seguinte)",
		],
		s12: [
			"Gestão do ecossistema (rede de parceiros, integrações, comunidade de desenvolvedores)",
			"Expansão de mercado (expansão geográfica ou para novos segmentos)",
			"Melhoria da qualidade do serviço (confiabilidade, desempenho, qualidade do suporte)",
			"Preparação organizacional (competências da equipe, processos, prontidão interna)",
			"Orientação baseada em valor (foco em entregar valor mensurável ao cliente)",
			"Outro (especifique no campo seguinte)",
		],
		s13: [
			"Preocupações com segurança (proteção de dados, conformidade, vulnerabilidades)",
			"Transformação de fluxo de receita (transição de modelo de precificação ou receita)",
			"Manutenção da confiança do cliente (transparência, confiabilidade, retenção)",
			"Disrupção do ecossistema de parceiros (impacto em revendedores, integradores)",
			"Prontidão organizacional (resistência interna, lacunas de competências)",
			"Gestão de qualidade (manter qualidade durante escala ou transições)",
			"Outro (especifique no campo seguinte)",
		],
		s14: [
			"Estratégia de precificação flexível (ajustar preços para reduzir churn ou atrair segmentos)",
			"Adoção de modelo híbrido (combinar modelos de entrega ou receita para transição gradual)",
			"Implementação piloto (testar mudanças com um subconjunto de clientes antes do rollout completo)",
			"Compensação de parceiros (oferecer incentivos ou suporte para mitigar disrupção de parceiros)",
			"Outro (especifique no campo seguinte)",
		],
	};
}

/**
 * @param {string} locale 'pt' (default) or 'en'
 * @return {GoogleAppsScript.Forms.Form} the created form
 */
function createSBMOValidationForm_(locale) {
	if (locale !== "en" && locale !== "pt") {
		locale = "pt";
	}
	var t = getFormStrings_(locale);
	var c = getChoiceGroups_(locale);

	var form = FormApp.create(t.formTitle);
	form.setDescription(t.formDescription);
	form.setIsQuiz(false);
	form.setAllowResponseEdits(true);
	form.setCollectEmail(true);
	form.setLimitOneResponsePerUser(false);
	form.setProgressBar(true);

	// ——— TCLE / Informed consent (primeiro bloco, sem page break vazio no topo) ———
	form
		.addSectionHeaderItem()
		.setTitle(t.tcleSectionTitle)
		.setHelpText(t.tcleBody);
	form
		.addCheckboxItem()
		.setTitle(t.consentItemTitle)
		.setChoiceValues([t.consentCheckbox])
		.setRequired(true);

	// ——— Section 1: identification + operational status ———
	form.addPageBreakItem().setTitle(t.s1Title).setHelpText(t.s1Help);
	form
		.addTextItem()
		.setTitle(t.company)
		.setHelpText(t.companyHelp)
		.setRequired(true);
	form
		.addTextItem()
		.setTitle(t.product)
		.setHelpText(t.productHelp)
		.setRequired(true);
	form
		.addTextItem()
		.setTitle(t.year)
		.setHelpText(t.yearHelp)
		.setRequired(false);
	form
		.addParagraphTextItem()
		.setTitle(t.bmodel)
		.setHelpText(t.bmodelHelp)
		.setRequired(true);
	form
		.addTextItem()
		.setTitle(t.respondent)
		.setHelpText(t.respondentHelp)
		.setRequired(true);
	form
		.addMultipleChoiceItem()
		.setTitle(t.operational)
		.setHelpText(t.operationalHelp)
		.setChoiceValues([t.opYes, t.opNo, t.opPartial])
		.setRequired(true);

	// ——— Sections 2–15 ———
	form.addPageBreakItem().setTitle(t.s2Title).setHelpText(t.s2Help);
	form
		.addCheckboxItem()
		.setTitle(t.s2Q)
		.setHelpText(t.s2QHelp)
		.setChoiceValues(c.s2)
		.setRequired(true);
	form
		.addTextItem()
		.setTitle(t.s2Other)
		.setHelpText(t.s2OtherHelp)
		.setRequired(false);

	form.addPageBreakItem().setTitle(t.s3Title).setHelpText(t.s3Help);
	form
		.addCheckboxItem()
		.setTitle(t.s3Q)
		.setChoiceValues(c.s3)
		.setRequired(true);
	form.addTextItem().setTitle(t.s3Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s4Title).setHelpText(t.s4Help);
	form
		.addCheckboxItem()
		.setTitle(t.s4Q)
		.setChoiceValues(c.s4)
		.setRequired(true);
	form.addTextItem().setTitle(t.s4Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s5Title).setHelpText(t.s5Help);
	form
		.addCheckboxItem()
		.setTitle(t.s5Q)
		.setChoiceValues(c.s5)
		.setRequired(true);
	form.addTextItem().setTitle(t.s5Other).setRequired(false);
	form
		.addTextItem()
		.setTitle(t.s5Period)
		.setHelpText(t.s5PeriodHelp)
		.setRequired(false);
	form
		.addParagraphTextItem()
		.setTitle(t.s5Desc)
		.setHelpText(t.s5DescHelp)
		.setRequired(false);

	form.addPageBreakItem().setTitle(t.s6Title).setHelpText(t.s6Help);
	form
		.addCheckboxItem()
		.setTitle(t.s6Q)
		.setChoiceValues(c.s6)
		.setRequired(true);
	form.addTextItem().setTitle(t.s6Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s7Title).setHelpText(t.s7Help);
	form
		.addCheckboxItem()
		.setTitle(t.s7Q)
		.setChoiceValues(c.s7)
		.setRequired(true);
	form.addTextItem().setTitle(t.s7Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s8Title).setHelpText(t.s8Help);
	form
		.addCheckboxItem()
		.setTitle(t.s8Q)
		.setChoiceValues(c.s8)
		.setRequired(true);
	form.addTextItem().setTitle(t.s8Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s9Title).setHelpText(t.s9Help);
	form
		.addCheckboxItem()
		.setTitle(t.s9Q)
		.setChoiceValues(c.s9)
		.setRequired(false);
	form.addTextItem().setTitle(t.s9Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s10Title).setHelpText(t.s10Help);
	form
		.addCheckboxItem()
		.setTitle(t.s10Q)
		.setChoiceValues(c.s10)
		.setRequired(false);
	form.addTextItem().setTitle(t.s10Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s11Title).setHelpText(t.s11Help);
	form
		.addCheckboxItem()
		.setTitle(t.s11Q)
		.setChoiceValues(c.s11)
		.setRequired(false);
	form.addTextItem().setTitle(t.s11Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s12Title).setHelpText(t.s12Help);
	form
		.addCheckboxItem()
		.setTitle(t.s12Q)
		.setChoiceValues(c.s12)
		.setRequired(false);
	form.addTextItem().setTitle(t.s12Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s13Title).setHelpText(t.s13Help);
	form
		.addCheckboxItem()
		.setTitle(t.s13Q)
		.setChoiceValues(c.s13)
		.setRequired(false);
	form.addTextItem().setTitle(t.s13Other).setRequired(false);

	form.addPageBreakItem().setTitle(t.s14Title).setHelpText(t.s14Help);
	form
		.addCheckboxItem()
		.setTitle(t.s14Q)
		.setChoiceValues(c.s14)
		.setRequired(false);
	form.addTextItem().setTitle(t.s14Other).setRequired(false);
	form
		.addParagraphTextItem()
		.setTitle(t.s14Map)
		.setHelpText(t.s14MapHelp)
		.setRequired(false);

	form.addPageBreakItem().setTitle(t.s15Title).setHelpText(t.s15Help);
	form
		.addParagraphTextItem()
		.setTitle(t.s15Q)
		.setHelpText(t.s15QHelp)
		.setRequired(false);
	form
		.addMultipleChoiceItem()
		.setTitle(t.s15Follow)
		.setChoiceValues([t.s15Y, t.s15N, t.s15M])
		.setRequired(false);

	form.setConfirmationMessage(t.confirmation);

	Logger.log("Form created (" + locale + "): " + t.formTitle);
	Logger.log("Edit URL: " + form.getEditUrl());
	Logger.log("Published URL: " + form.getPublishedUrl());

	return form;
}

/** Alias: mesmo que createSBMOValidationFormPT() (mantido para o fluxo documentado no cabeçalho). */
function createSBMOValidationForm() {
	return createSBMOValidationForm_("pt");
}

function createSBMOValidationFormPT() {
	return createSBMOValidationForm_("pt");
}

function createSBMOValidationFormEN() {
	return createSBMOValidationForm_("en");
}

/**
 * Cria os dois formulários (pt-BR e EN) e registra as URLs no log.
 * @return {{pt: GoogleAppsScript.Forms.Form, en: GoogleAppsScript.Forms.Form}}
 */
function createSBMOValidationFormAll() {
	var pt = createSBMOValidationForm_("pt");
	var en = createSBMOValidationForm_("en");
	Logger.log("=== PT-BR form published: " + pt.getPublishedUrl());
	Logger.log("=== EN form published: " + en.getPublishedUrl());
	return { pt: pt, en: en };
}
