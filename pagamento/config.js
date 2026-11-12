/* Public checkout configuration. Never put API keys or secrets in this file.
 * Fill only with verified provider links for the matching plan and amount.
 * mode: "recurring" for an actual monthly subscription;
 *       "one_time" for payment of the first month only.
 * Keep enabled:false until provider, pricing and legal terms are ready.
 * This static redirect does not confirm payment or activate the service.
 */
window.NELIS_PAYMENTS = Object.freeze({
  assinatura: { enabled: true, url: "https://pay.kiwify.com.br/rpda7kg", mode: "recurring", provider: "Kiwify" },
  essencial: { enabled: true, url: "https://pay.kiwify.com.br/tGS9Y2j", mode: "recurring", provider: "Kiwify" },
  assistida: { enabled: true, url: "https://pay.kiwify.com.br/uMB0K4T", mode: "recurring", provider: "Kiwify" },
  presenca: { enabled: true, url: "https://pay.kiwify.com.br/ncYVSit", mode: "recurring", provider: "Kiwify" }
});
