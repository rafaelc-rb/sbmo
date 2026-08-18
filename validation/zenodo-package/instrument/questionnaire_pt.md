# Questionário de Validação da SBMO (instrumento, português)

*Apenas a estrutura, sem respostas. Transcrição verbatim confirmada em
2026-08-18 contra um PDF exportado do formulário real efetivamente usado na
coleta ("SBMO - Validação de Modelo de Negócio de Software - Google
Formulários.pdf", 13 páginas), que bateu exatamente com o script gerador
`sbmo/scripts/sbmo_create_individual_form.gs` em todas as 15 seções, 40
perguntas, textos de ajuda e opções. O formulário começa com o campo de
e-mail (obrigatório) e o Termo de Consentimento (ver
`../informed_consent/informed_consent_pt.md`), seguido destas 15 seções.
Tempo estimado: 15 a 20 minutos. As Seções 9, 10 e 11 são opcionais; as
demais são obrigatórias. Perguntas de múltipla escolha marcadas "Selecione
todas as opções que se aplicam" (Seção 2 exige pelo menos uma opção).*

**Campo inicial:** E-mail (obrigatório).

## 1. Identificação da Empresa e do Produto

Informações básicas para identificar a empresa e seu principal produto ou serviço de software.

- **Nome da empresa** (obrigatório): Nome oficial da empresa. *(uso administrativo apenas, não publicado)*
- **Nome do produto ou serviço** (obrigatório): Nome do principal produto ou serviço de software oferecido. *(não publicado)*
- **Ano de lançamento** (opcional): Ano em que o produto/serviço foi lançado ou disponibilizado pela primeira vez (ex.: 2018).
- **Descrição breve do modelo de negócio** (obrigatório): Em 2 a 4 frases, descreva como esse produto/serviço gera valor e receita. Exemplo: "Oferecemos uma plataforma SaaS B2B para gestão de projetos, vendida por assinaturas mensais com um plano gratuito para equipes pequenas."
- **Nome e cargo do respondente** (obrigatório): Seu nome e cargo na empresa (ex.: "João Silva, CTO"). *(não publicado; apenas a parte do cargo é usada, em categorias agregadas, na análise sócio-demográfica)*
- **Qual o seu conhecimento sobre o modelo de negócio deste produto/serviço?** (obrigatório): escala 1 (Não) a 5 (Conheço muito bem).
- **O modelo de negócio deste produto/serviço já está operacional?** (obrigatório): Sim / Não / Parcialmente. Se "Não" ou "Parcialmente", responder com base no cenário planejado para os próximos 12 meses.

## 2. Tipo de Produto ou Serviço *(obrigatório; selecione todas que se aplicam, pelo menos uma)*
Aplicação; Plataforma; Serviço gerenciado; Serviço de API; Produto de dados; Infraestrutura; SDK / Kit de desenvolvimento; Outro (especifique).

## 3. Modo de Entrega *(obrigatório; selecione todas que se aplicam)*
SaaS multi-tenant; SaaS single-tenant; On-premises; Entrega mobile; Entrega desktop; Entrega híbrida; Outro (especifique).

## 4. Fontes de Receita *(obrigatório; selecione todas que se aplicam)*
Receita por assinatura; Receita por uso/consumo; Receita por transação; Receita por publicidade; Receita por licença perpétua; Receita por suporte; Taxa de marketplace; Receita open core; Receita por licenciamento dual; Outro (especifique).

## 5. Estratégia de Precificação *(obrigatório; selecione todas que se aplicam)*
Precificação por assinatura; Precificação pay-as-you-go; Precificação freemium; Precificação baseada em valor; Precificação baseada em custo; Outro (especifique).
Também coleta: **Periodicidade de cobrança** (texto livre, opcional; ex.: mensal, anual, por transação) e **Descrição da precificação** (texto livre, opcional; ex.: "Temos 3 planos: Grátis, Pro (R$99/mês), Enterprise (preço sob consulta).").

## 6. Tipo de Cliente *(obrigatório; selecione todas que se aplicam)*
B2B; B2C; PMEs; Enterprise; Governo; Ferramentas para desenvolvedores; Outro (especifique).

## 7. Papel no Ecossistema *(obrigatório; selecione todas que se aplicam)*
Produto standalone; Plataforma bilateral; Marketplace; Componente OEM; Plugin / complemento; Outro (especifique).

## 8. Canal de Aquisição *(obrigatório; selecione todas que se aplicam)*
Venda direta; Crescimento liderado pelo produto; Canal de parceiros; Marketing digital; Canal de marketplace; Indicação; Outro (especifique).

## 9. Regime de Propriedade Intelectual *(opcional; selecione todas que se aplicam)*
Proprietário; Open source permissivo (MIT, Apache, BSD); Open source (geral); Licença dual; Open core; Copyleft (GPL, AGPL); Outro (especifique).

## 10. Unidade Base de Precificação *(opcional; selecione todas que se aplicam)*
Usuário / licença; Baseado em transação; Tempo de computação; Compartilhamento de receita; Chamadas de API; Armazenamento; Dispositivo; Outro (especifique).

## 11. Efeitos de Rede *(opcional; selecione todas que se aplicam)*
Efeito de rede direto; Efeito de rede cruzado; Efeito de rede orientado a dados; Sem efeitos de rede significativos; Outro (especifique).

## 12. Fatores de Sucesso *(obrigatório; selecione todas que se aplicam)*
Gestão do ecossistema; Expansão de mercado; Melhoria da qualidade do serviço; Preparação organizacional; Orientação baseada em valor; Outro (especifique).

## 13. Desafios de Implementação *(obrigatório; selecione todas que se aplicam)*
Preocupações com segurança; Transformação de fluxo de receita; Manutenção da confiança do cliente; Disrupção do ecossistema de parceiros; Prontidão organizacional; Gestão de qualidade; Outro (especifique).

## 14. Estratégias de Mitigação *(obrigatório; selecione todas que se aplicam)*
Estratégia de precificação flexível; Adoção de modelo híbrido; Implementação piloto; Compensação de parceiros; Outro (especifique).
Também coleta: **Qual desafio cada mitigação endereça?** (texto livre, opcional). Exemplo dado no formulário: "Precificação flexível → Transformação de fluxo de receita; Piloto → Segurança".

## 15. Comentários Adicionais
- **Comentários ou observações adicionais** (texto livre, opcional): Existe algum aspecto do modelo de negócio de software da sua empresa que não foi coberto pelas perguntas acima? Alguma dimensão que você considera importante e que estava faltando?
- **Você estaria disponível para uma breve conversa de acompanhamento (15 a 20 min) para esclarecer respostas?** (opcional): Sim / Não / Talvez.

---

Cada uma das 13 perguntas de vocabulário controlado (Seções 2 a 14, exceto os dois campos de texto livre nas Seções 5 e 14) mapeia diretamente para uma dimensão da ontologia SBMO; ver `../data/data_dictionary.md` para o mapeamento completo rótulo -> classe usado na construção de `../data/cases_normalized.csv`.
