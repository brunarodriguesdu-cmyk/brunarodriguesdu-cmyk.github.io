# Contratação da Nelis

A página `/pagamento/?plano=essencial` aceita também `assistida` e `presenca`. Sem plano ou com identificador inválido, solicita uma seleção. O preço nunca é lido da URL.

## Conectar o provedor

Editar `config.js`, que é público e não pode conter credenciais. Para cada plano:

1. Criar um checkout real no provedor com o plano e valor corretos.
2. Conferir taxas, meios de pagamento, validade/reutilização do link e condições comerciais.
3. Definir `mode: "recurring"` somente se a cobrança mensal automática estiver de fato configurada; para uma cobrança do primeiro mês, usar `mode: "one_time"`.
4. Preencher `url` com o endereço HTTPS do checkout e o nome em `provider`.
5. Finalizar os textos legais existentes e validar uma transação no ambiente de teste do provedor antes de habilitar vendas.
6. Mudar `enabled` para `true` quando estiver pronto.

Sem configuração válida, a página mostra pagamento online em breve e contato pelo WhatsApp. Não coleta dados pessoais nem dados de cartão, não simula aprovação e não ativa acesso.

O redirecionamento não confirma pagamento. Para ativação automática da assistente será necessário um backend que valide notificações do provedor, associe a transação ao cliente/plano e controle pagamentos pendentes, aprovados, cancelados e reembolsados. Uma URL de retorno não é prova de pagamento.

Os valores e condições refletem os pacotes da página principal: R$ 197, R$ 397 e R$ 597 por mês, sem fidelidade (cancelamento livre). Ao mudar ofertas, atualizar também `checkout.js`, os rótulos de `index.html` desta pasta, a página inicial e os links no provedor.
